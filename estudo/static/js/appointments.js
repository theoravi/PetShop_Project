// static/js/appointments.js

document.addEventListener('DOMContentLoaded', function() {
  // Inicializa o Tempus Dominus no campo com visual de calendário e relógio
  new tempusDominus.TempusDominus(document.getElementById('dtpicker'), {
    display: {
      components: {
        calendar: true,
        date: true,
        clock: true,
        hours: true,
        minutes: true
      },
      icons: {
        type: 'icons',
        date: 'bi bi-calendar-date',
        clock: 'bi bi-clock',
        up: 'bi bi-chevron-up',
        down: 'bi bi-chevron-down',
        previous: 'bi bi-chevron-left',
        next: 'bi bi-chevron-right',
        today: 'bi bi-calendar-check',
        clear: 'bi bi-trash',
        close: 'bi bi-x'
      }
    },
    localization: {
      locale: 'pt-BR',
      format: 'dd-MM-yyyy HH:mm'
    }
  });

  // Exibe a máscara no padrão americano (MM/DD/YYYY HH:mm)
  $('#dateTimeInput').inputmask({
    mask: "99/99/9999 99:99",
    placeholder: "MM/DD/YYYY HH:mm",
    alias: "datetime",
    hourFormat: "24"
  });

  // Recupera o mapa de pets por cliente que foi renderizado no template
  const petsByCustomer = JSON.parse(document.getElementById('pets-data').textContent);
  const customerSelect = document.getElementById('customerSelect');
  const petSelect = document.getElementById('petSelect');

  customerSelect.addEventListener('change', function() {
    const pets = petsByCustomer[this.value] || [];
    petSelect.innerHTML = '';
    if (pets.length) {
      pets.forEach(p => petSelect.append(new Option(p.name, p.id)));
    } else {
      const opt = new Option('Nenhum pet para este cliente', '');
      petSelect.appendChild(opt);
    }
  });

  // Desencadeia um 'change' inicial para popular o campo de pets assim que a página carrega
  customerSelect.dispatchEvent(new Event('change'));
});
