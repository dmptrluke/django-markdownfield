document.addEventListener("DOMContentLoaded",function() {
    const fields = document.querySelectorAll('.data-easymde');
    fields.forEach((field) => {
        new EasyMDE({
            element: field,
            hideIcons: ["side-by-side", "preview"],
            spellChecker: false,
            parsingConfig: {
                allowAtxHeaderWithoutSpace: true,
            }
        });
    });
});