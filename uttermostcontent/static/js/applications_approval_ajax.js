(function($) {
    $(document).ready(function() {
        $('#id_Application_id').change(function() {
            var appId = $(this).val();
            $.ajax({
                url: '/admin/uttermostcontent/get_user_for_application/',
                data: {'app_id': appId},
                dataType: 'json',
                success: function(data) {
                    $('#id_user').val(data.user_id).attr('readonly', 'readonly');
                },
                error: function(xhr, textStatus, errorThrown) {
                    console.error('Error:', errorThrown);
                }
            });
        });
    });
})(django.jQuery);
