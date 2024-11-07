document.addEventListener("DOMContentLoaded", function() {
    const planSections = document.querySelectorAll('.registroPlanSeccion');

    planSections.forEach(plan => {
        plan.addEventListener('click', function() {
            const contrato = plan.querySelector('.registroPlanTitulo').textContent;

            document.querySelectorAll('.registroValor')[0].textContent = contrato;
        });
    });
});
