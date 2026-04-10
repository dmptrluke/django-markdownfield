/**
 * markdownfield.js
 *
 * Finds textarea[data-markdownfield] elements, reads their JSON config,
 * and initializes an EasyMDE instance for each. MutationObserver handles
 * dynamically added editors (formsets, HTMX swaps).
 */
(function () {
    'use strict';

    // Expose CodeMirror globally so optional CM5 language mode scripts
    // can register. Our custom EasyMDE build exports it as EasyMDE.CodeMirror.
    if (typeof EasyMDE !== 'undefined' && EasyMDE.CodeMirror) {
        window.CodeMirror = EasyMDE.CodeMirror;
    }

    var plugins = [];
    var instances = [];
    var scanTimer = null;

    // --- Table overlay (CM5) ---
    // EasyMDE doesn't tokenize table syntax at all.
    // This overlay adds cm-mdf-table-pipe, cm-mdf-table-sep, cm-mdf-table-cell
    // for monospace rendering and dimmed cell content.
    var tableOverlay = {
        token: function (stream) {
            if (stream.sol()) {
                if (!/^\s*\|/.test(stream.string)) {
                    stream.skipToEnd();
                    return null;
                }
            }
            if (stream.match(/^\|/)) { return 'mdf-table-pipe'; }
            if (stream.match(/^[\s:-]+(?=\|)/)) { return 'mdf-table-sep'; }
            if (stream.match(/^[^|]+/)) { return 'mdf-table-cell'; }
            stream.next();
            return null;
        }
    };

    // --- Code block line styling (CM5) ---
    // Lines inside a fenced code block get mdf-code-line for monospace styling.
    // The markdown parser tracks fenced blocks via fencedEndRE in its state.
    function attachCodeLineClasses(cm) {
        cm.on('renderLine', function (cm, line, el) {
            var lineNo = cm.getLineNumber(line);
            var state = cm.getStateAfter(lineNo, true);
            var inner = state.base || state;
            if (inner.fencedEndRE) {
                el.classList.add('mdf-code-line');
            }
        });
    }

    // --- CSRF cookie extraction (for preview) ---
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // --- Toolbar mapping ---
    function buildToolbar(toolbar, previewConfig) {
        var result = toolbar.map(function (item) {
            // EasyMDE uses button names as CSS classes; 'table' conflicts with Bootstrap's .table
            if (item === 'table') {
                return {
                    name: 'mdf-table',
                    action: EasyMDE.drawTable,
                    className: 'fa fa-table',
                    title: 'Insert Table'
                };
            }
            return item;
        });
        if (previewConfig) {
            // inject preview before the last separator group
            var lastSep = result.lastIndexOf('|');
            if (lastSep !== -1) {
                result.splice(lastSep, 0, 'preview');
            } else {
                result.push('|', 'preview');
            }
        }
        return result;
    }

    // --- Preview render factory ---
    function makePreviewRender(previewConfig) {
        var debounceTimer = null;
        return function (plainText, preview) {
            preview.innerHTML = 'Loading preview\u2026';
            clearTimeout(debounceTimer);
            debounceTimer = setTimeout(function () {
                var body = new URLSearchParams();
                body.append('text', plainText);
                body.append('validator', previewConfig.validator);
                fetch(previewConfig.url, {
                    method: 'POST',
                    headers: {'X-CSRFToken': getCookie('csrftoken')},
                    body: body,
                })
                .then(function (r) { return r.json(); })
                .then(function (data) {
                    if (data.html !== undefined) {
                        preview.innerHTML = data.html;
                    } else {
                        preview.textContent = data.error || 'Preview failed';
                    }
                })
                .catch(function () { preview.textContent = plainText; });
            }, 300);
            return 'Loading preview\u2026';
        };
    }

    // --- Init a single editor ---
    function initEditor(textarea) {
        var configId = textarea.getAttribute('data-markdownfield');
        var configEl = document.getElementById(configId);
        if (!configEl) {
            console.warn('markdownfield: config element not found:', configId);
            return;
        }

        var config;
        try {
            config = JSON.parse(configEl.textContent);
        } catch (e) {
            console.warn('markdownfield: invalid config JSON:', configId, e);
            return;
        }

        var toolbar = buildToolbar(config.toolbar || [], config.preview);

        var editorOptions = {
            element: textarea,
            toolbar: toolbar,
            parsingConfig: {
                allowAtxHeaderWithoutSpace: true
            }
        };

        if (config.preview) {
            editorOptions.previewRender = makePreviewRender(config.preview);
        }

        // user-provided options override everything (intentional)
        if (config.options) {
            Object.assign(editorOptions, config.options);
        }

        var mde;
        try {
            mde = new EasyMDE(editorOptions);
        } catch (e) {
            console.error('markdownfield: EasyMDE init failed:', e);
            return;
        }

        mde.codemirror.addOverlay(tableOverlay);
        attachCodeLineClasses(mde.codemirror);

        for (var i = 0; i < plugins.length; i++) {
            try { plugins[i](mde); } catch (e) {
                console.error('markdownfield: plugin error:', e);
            }
        }

        instances.push({textarea: textarea, mde: mde});
        textarea.setAttribute('data-markdownfield-init', '1');
    }

    // --- Scan for uninitialized editors ---
    function scan() {
        var targets = document.querySelectorAll(
            'textarea[data-markdownfield]:not([data-markdownfield-init])'
        );
        for (var i = 0; i < targets.length; i++) {
            initEditor(targets[i]);
        }
    }

    // --- Debounced scan for MutationObserver ---
    function debouncedScan() {
        if (scanTimer) { return; }
        scanTimer = setTimeout(function () {
            scanTimer = null;
            scan();
        }, 50);
    }

    // --- Public(ish) API ---
    window.markdownfield = {
        scan: scan,
        registerPlugin: function (fn) {
            plugins.push(fn);
            for (var i = 0; i < instances.length; i++) {
                try { fn(instances[i].mde); } catch (e) {
                    console.error('markdownfield: plugin error:', e);
                }
            }
        }
    };

    // --- Bootstrap ---
    if (document.body) {
        new MutationObserver(function () {
            debouncedScan();
        }).observe(document.body, {childList: true, subtree: true});
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', scan);
    } else {
        scan();
    }
})();
