/**
 * mte-kernel plugin for markdownfield.
 * Provides tab-to-next-cell, auto-formatting, and row/column navigation
 * when the cursor is inside a markdown table.
 *
 * Requires mte-kernel.min.js to be loaded first (exposes window.mteKernel).
 */
(function () {
    'use strict';

    // CM5 adapter implementing mte-kernel's ITextEditor interface
    function CM5TextEditor(cm) {
        this._cm = cm;
    }

    CM5TextEditor.prototype = Object.create(mteKernel.ITextEditor.prototype);

    CM5TextEditor.prototype.getCursorPosition = function () {
        var cur = this._cm.getCursor();
        return new mteKernel.Point(cur.line, cur.ch);
    };

    CM5TextEditor.prototype.setCursorPosition = function (pos) {
        this._cm.setCursor({line: pos.row, ch: pos.column});
    };

    CM5TextEditor.prototype.setSelectionRange = function (range) {
        this._cm.setSelection(
            {line: range.start.row, ch: range.start.column},
            {line: range.end.row, ch: range.end.column}
        );
    };

    CM5TextEditor.prototype.getLastRow = function () {
        return this._cm.lineCount() - 1;
    };

    CM5TextEditor.prototype.acceptsTableEdit = function (row) {
        // reject rows inside fenced code blocks
        var token = this._cm.getTokenAt({line: row, ch: 0});
        if (token && token.type) {
            var types = token.type.split(' ');
            if (types.indexOf('comment') !== -1) return false;
        }
        return true;
    };

    CM5TextEditor.prototype.getLine = function (row) {
        return this._cm.getLine(row);
    };

    CM5TextEditor.prototype.insertLine = function (row, line) {
        var lastRow = this._cm.lineCount() - 1;
        if (row > lastRow) {
            this._cm.replaceRange('\n' + line, {line: lastRow, ch: this._cm.getLine(lastRow).length});
        } else {
            this._cm.replaceRange(line + '\n', {line: row, ch: 0});
        }
    };

    CM5TextEditor.prototype.deleteLine = function (row) {
        var lastRow = this._cm.lineCount() - 1;
        if (row >= lastRow) {
            // last line: delete from end of previous line
            if (row > 0) {
                this._cm.replaceRange('', {line: row - 1, ch: this._cm.getLine(row - 1).length}, {line: row, ch: this._cm.getLine(row).length});
            } else {
                this._cm.replaceRange('', {line: 0, ch: 0}, {line: 0, ch: this._cm.getLine(0).length});
            }
        } else {
            this._cm.replaceRange('', {line: row, ch: 0}, {line: row + 1, ch: 0});
        }
    };

    CM5TextEditor.prototype.replaceLines = function (startRow, endRow, lines) {
        var endLine = this._cm.getLine(endRow - 1);
        this._cm.replaceRange(
            lines.join('\n'),
            {line: startRow, ch: 0},
            {line: endRow - 1, ch: endLine.length}
        );
    };

    CM5TextEditor.prototype.transact = function (func) {
        this._cm.operation(func);
    };

    // default mte-kernel options
    var mteOptions = mteKernel.options({
        smartCursor: true
    });

    /**
     * Attach table editing keybindings to an EasyMDE instance.
     * Call after constructing the EasyMDE editor.
     */
    function attachTableEditor(easymde) {
        var cm = easymde.codemirror;
        var adapter = new CM5TextEditor(cm);
        var te = new mteKernel.TableEditor(adapter);

        // reset smart cursor when cursor moves outside a table or on mouse click
        cm.on('cursorActivity', function () {
            if (!te.cursorIsInTable(mteOptions)) {
                te.resetSmartCursor();
            }
        });

        var extraKeys = cm.getOption('extraKeys') || {};

        extraKeys['Tab'] = function () {
            if (te.cursorIsInTable(mteOptions)) {
                te.nextCell(mteOptions);
            } else {
                // default: insert spaces
                cm.execCommand('defaultTab');
            }
        };

        extraKeys['Shift-Tab'] = function () {
            if (te.cursorIsInTable(mteOptions)) {
                te.previousCell(mteOptions);
            } else {
                cm.execCommand('indentLess');
            }
        };

        extraKeys['Enter'] = function () {
            if (te.cursorIsInTable(mteOptions)) {
                te.nextRow(mteOptions);
            } else {
                cm.execCommand('newlineAndIndent');
            }
        };

        extraKeys['Escape'] = function () {
            if (te.cursorIsInTable(mteOptions)) {
                te.escape(mteOptions);
            } else if (easymde.isFullscreenActive()) {
                easymde.toggleFullScreen();
            }
        };

        // ctrl/cmd+shift+f to format the table under the cursor
        extraKeys['Ctrl-Shift-F'] = function () {
            if (te.cursorIsInTable(mteOptions)) {
                te.format(mteOptions);
            }
        };

        extraKeys['Cmd-Shift-F'] = function () {
            if (te.cursorIsInTable(mteOptions)) {
                te.format(mteOptions);
            }
        };

        cm.setOption('extraKeys', extraKeys);
    }

    // register with markdownfield.js plugin system
    if (window.markdownfield) {
        markdownfield.registerPlugin(attachTableEditor);
    }
})();
