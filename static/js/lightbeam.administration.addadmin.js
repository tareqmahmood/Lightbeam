/**
 * Created by HP on 22-May-17.
 */


function changeRole(user_id, role) {

    $.ajax({
        type: "POST",
        url: "/administration-change-role/",
        dataType: "json",
        success: function (status) {
            if(status)
            {
                location.reload();
            }
            else
            {

            }
        },
        data: {
            user_id: user_id,
            role: role,
            csrfmiddlewaretoken: getCookie('csrftoken')
        }
    });
}