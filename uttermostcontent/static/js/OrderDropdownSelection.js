$("#institute").change(function () {
    const url1 = $("#discipline").attr("discipline-queries-url");
    const url2 = $("#teacher").attr("teacher-queries-url");
    const instituteId = $(this).val();                // get the selected institute ID from the HTML input
    $.ajax({                                          // initialize an AJAX request
        url: url1,                                    // set the url of the request (= ajax/load-discipline-details/ )
        data: { 'institute_id': instituteId },        // add the institute id to the GET parameters
        success: function (data) {
            $("#discipline").html(data);
        }
    });
    $.ajax({
        url: url2,
        data: { 'institute_id': instituteId },
        success: function (data) {
            $("#teacher").html(data);
        }
    })
});

$("#discipline").change(function () {
    const url = $("#macro_content").attr("macro-queries-url");
    const disciplineID = $(this).val();
    $.ajax({
        url: url,
        data: { 'discipline_id': disciplineID },
        success: function (data) {
            $("#macro_content").html(data);
        }
    });
});

$("#macro_content").change(function () {
    const url = $("#micro_content").attr("micro-queries-url");
    const macro_contentID = $(this).val();
    $.ajax({
        url: url,
        data: { 'disciplinemacrocontent_id': macro_contentID },
        success: function (data) {
            $("#micro_content").html(data);
        }
    });
});