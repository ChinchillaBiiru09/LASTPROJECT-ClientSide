$(".tab-wizard").steps({
	headerTag: "h5",
	bodyTag: "section",
	transitionEffect: "fade",
	titleTemplate: '<span class="step">#index#</span> #title#',
	labels: {
		finish: "Submit"
	},
	onStepChanged: function (event, currentIndex, priorIndex) {
		$('.steps .current').prevAll().addClass('disabled');
	},
	onFinished: function (event, currentIndex) {
        var payload = {
            nama: $('#category').val(),
            // harga: $('#harga').val(),
            // id_kategori: $('#id_kategori').val(),
            // is_stok_satuan: Number($("#is_stok_satuan").val()),
            // foto: localStorage.getItem('fileInputBase64')
        };

        // Set API Request Configuration
        var myHeaders = new Headers();
        var raw = JSON.stringify(payload);
        myHeaders.append("Content-Type", "application/json");
        var requestOptions = {
            method: 'POST',
            headers: myHeaders,
            body: raw,
            redirect: 'follow'
        };

        // Set Loading UI
        swal({
            title: 'Tunggu Sebentar..',
            text: "Permintaan kamu sedang diproses",
            button: false
        });

        // Request API
        fetch(`${BASE_URL}/manage/invitation/add`, requestOptions)
            .then(response => response.json())
            .then(response => {
                if (response.status_code == 200) {
            		$('#success-modal').modal('show');        
                }
                else {
                    swal({
                        title: `${response.description}`,
                        icon: "error",
                        buttons: {
                            tutup: {
                                className: "btn bg-gradient-danger",
                                text: "Kembali",
                                value: 0
                            },
                            lanjut: {
                                className: "btn bg-gradient-info",
                                text: "Buat Kategori Baru lainnya",
                                value: 1
                            }
                        }
                    }).then((buat_kategori_lagi) => {
                        if (buat_kategori_lagi) {
                            createKategoriBaru()
                        }
                        else {
                            // auto refresh halaman agar user dapat melihat daftar kategori produk terbaru
                            window.location.replace(`${BASE_URL}/dashboard/manajemen/kategori`);
                        }
                    });
                }
            })
            .catch(error => console.log('error', error));
	}
});

document.addEventListener('DOMContentLoaded', function() {
    // const categorySelect = document.getElementById('category');
    // const templateContainer = document.getElementById('templateContainer');

    const templates = {
        1: [
            { name: "Template 1", image: "vendors/images/photo1.jpg", description: "Description 1" },
            { name: "Template 2", image: "vendors/images/photo2.jpg", description: "Description 2" }
        ],
        2: [
            { name: "Template 3", image: "vendors/images/photo3.jpg", description: "Description 3" },
            { name: "Template 4", image: "vendors/images/photo4.jpg", description: "Description 4" }
        ]
        // Tambahkan category dan template lainnya sesuai kebutuhan
    };

    categorySelect.addEventListener('change', function() {
        const selectedCategory = categorySelect.value;
        templateContainer.innerHTML = '';

        if (templates[selectedCategory]) {
            templates[selectedCategory].forEach(template => {
                const templateDiv = document.createElement('div');
                templateDiv.classList.add('col-lg-3', 'col-md-6', 'col-sm-12', 'mb-30');
                templateDiv.innerHTML = `
                    <div class="da-card">
                        <div class="da-card-photo">
                            <img src="${template.image}" alt="${template.name}">
                            <div class="da-overlay">
                                <div class="da-social">
                                    <ul class="clearfix">
                                        <li><a href="#"><i class="fa fa-facebook"></i></a></li>
                                        <li><a href="#"><i class="fa fa-twitter"></i></a></li>
                                        <li><a href="#"><i class="fa fa-envelope-o"></i></a></li>
                                    </ul>
                                </div>
                            </div>
                        </div>
                        <div class="da-card-content">
                            <h5 class="h5 mb-10">${template.name}</h5>
                            <p class="mb-0">${template.description}</p>
                        </div>
                    </div>
                `;
                templateContainer.appendChild(templateDiv);
            });
        }
    });
});
