(function ($) {
    "use strict";

    var SweetAlert = function () {};

    SweetAlert.prototype.init = function () {
        $(document).on('click', '.btn-delete', function () {
            var guestId = $(this).data('id');
            swal({
                title: 'Are you sure?',
                text: "You won't be able to revert this!",
                type: 'warning',
                showCancelButton: true,
                confirmButtonText: 'Yes, delete it!',
                cancelButtonText: 'No, cancel!',
                confirmButtonClass: 'btn btn-success margin-5',
                cancelButtonClass: 'btn btn-danger margin-5',
                buttonsStyling: false
            }).then(function () {
                // Here you should make an AJAX request to delete the item from the server
                var payload = {
                    guest_id: guestId
                };
        
                // Set API Request Configuration
                var myHeaders = new Headers();
                var raw = JSON.stringify(payload);
                myHeaders.append("Content-Type", "application/json");
                var requestOptions = {
                    method: 'GET',
                    headers: myHeaders,
                    body: raw,
                    redirect: 'follow'
                };

                // Debugging log
                console.log("payload:", raw);
                console.log("Sending request to:", `${BASE_URL}/guest/delete/tamu`);
                console.log("Request options:", requestOptions);
        
                // Request API Front End
                fetch(`${BASE_URL}/guest/delete/tamu`, requestOptions)
                    .then(response => {
                        console.log("Response received:", response);
                        return response.json().then(data => ({
                            status: response.status,
                            body: data
                        }));
                    })
                    .then(response => {
                        console.log('status code :', response.status_code)
                        if (response.status_code === 200) {
                            swal('Deleted!', 'Your file has been deleted.', 'success');
                            // Remove the row from the table
                            $('tr').has('a[data-id="' + categoryId + '"]').remove();
                        }
                        else {
                            swal('Error', `${response.description}`, 'error');
                        }
                    })
                    .catch(error => {
                        console.error('Fetch error:', error);
                        swal('Error', 'There was an error deleting the item.', 'error');
                    });
            }, function (dismiss) {
                if (dismiss === 'cancel') {
                    swal('Cancelled', 'Your imaginary file is safe :)', 'error');
                }
            });
        });
    };

    $.SweetAlert = new SweetAlert;
    $.SweetAlert.Constructor = SweetAlert;
})(window.jQuery);

(function ($) {
    "use strict";
    $.SweetAlert.init();
})(window.jQuery);
