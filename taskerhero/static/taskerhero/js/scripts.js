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

function toggleTag(tag_button, active_tags, task_table) {
    // tag_button: the action button linked to the tag to toggle
    // active_tags: a list of all tags to leave active; tasks will be left unhidden if they have *any* of the tags in the list
    // task_table: the table which contains the tasks to be toggled
    $(tag_button).toggleClass('btn-primary btn-default');
    if ($(tag_button).hasClass('btn-primary')) {
        active_tags.push(tag_button.text());
    } else {
        active_tags.splice($.inArray(tag_button.text(),active_tags), 1);
    }

    $(task_table).each(function (index, row) {
        // Ignore any task that is untagged; those should not toggle now
        if (!($(row).hasClass('untagged'))) {
            var has_active_tag = false;
            $.each(active_tags, function(index, tag_name) {
                if ($(row).hasClass('tag-' + tag_name)) {
                    has_active_tag = true;
                }
            if (has_active_tag) {
                $(row).removeClass('hidden');
            } else {
                $(row).addClass('hidden');
            }
            });
        }
    });

    updateStriping(task_table);

    return active_tags;
}

function toggleUntagged(untagged_button) {
    $(untagged_button).toggleClass('btn-primary btn-default');
    if ($(untagged_button).hasClass('btn-primary')) {
        $('.untagged').removeClass('hidden');
    } else {
        $('.untagged').addClass('hidden');
    }
}

function updateTag(add_tag, tag_name, task_pk, csrf_token, update_url, button_id) {
    // add_tag should be boolean; if false, tag will be removed
    // on success, returns the name of the tag that was changed
    // on fail, returns false
    if (add_tag) {
        data_dict = {add_tag: tag_name,
                     task_id: task_pk,
                     csrfmiddlewaretoken: csrf_token
                     };
    } else {
        data_dict = {remove_tag: tag_name,
                     task_id: task_pk,
                     csrfmiddlewaretoken: csrf_token
                     };
    }
    $.ajax({
        url: update_url,
        method: 'POST',
        data: data_dict
    }).done(function(json) {
        element_id = '#' + button_id
        $(element_id).toggleClass('btn-primary btn-default');
    }).fail(function(errorinfo) {
        console.log(errorinfo);
    });
}