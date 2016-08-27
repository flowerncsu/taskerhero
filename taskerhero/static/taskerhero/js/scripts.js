function updateStriping(table_to_update) {
    var count = 0;
    $(table_to_update).each(function (index, row) {
        if (!$(row).hasClass("hidden")) {
            if (count % 2 == 1) {
                $(row).addClass('table-color-1');
                $(row).removeClass('table-color-2');
            } else {
                $(row).addClass('table-color-2');
                $(row).removeClass('table-color-1');
            }
            count++;
        }
    });
}