const btnDelete = document.querySelectorAll('.btn-delete')

if (btnDelete) {
    const btnArray = Array.from(btnDelete);
    btnArray.forEach((btn) => {
        btn.addEventListener('click', (e) => {
            if(!confirm('Esta seguro de borrar el trabajo?')){
                e.preventDefault();
            }
        });
    });
}


$(document).ready(function() {
    $('#tabla_index').DataTable({
        "dom":'ftri',
        scrollY:        '30vh',
        scrollCollapse: true,
        "language": {
          "info":           "Hicimos _TOTAL_ trabajos",
          "search":         "Filtro _INPUT_ ",
        },
        "search": {
            "addClass": 'form-control input-lg col-xs-6'
        },
        
    });

   
} );