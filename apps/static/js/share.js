$('#message-modal').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget); // Button that triggered the modal
    var phone = button.data('phone'); // Extract info from data-* attributes
    var message = button.data('message'); // Extract info from data-* attributes
    var modal = $(this);
    modal.find('#to').val(phone); // Update the modal's input with the phone number
    modal.find('#message').val(message); // Update the modal's input with the phone number
});

function sendToWhatsApp() {
    // Ambil nomor telepon tujuan
    const phoneNumber = document.getElementById("to").value; // Ganti dengan nomor tujuan
    // Ambil pesan dari input form
    const message = document.getElementById("message").value;
    // const message = "cek send this message";
    // Encode pesan untuk URL
    const encodedMessage = encodeURIComponent(message);
    // Buat URL WhatsApp
    const whatsappURL = `https://wa.me/${phoneNumber}/?text=${encodedMessage}`;
    // Buka URL di tab/jendela baru
    window.open(whatsappURL, '_blank');
}