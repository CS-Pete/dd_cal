document.addEventListener('DOMContentLoaded', function () {
    const computeBtn = document.getElementById('compute-btn');
    const datePicker = document.getElementById('date-picker');
    const resultDiv = document.getElementById('result');
    const lapseLink = document.getElementById('lapse-link');
    const lapseHeading = document.getElementById('lapse-heading');

    // Enable Compute button when date is selected
    datePicker.addEventListener('input', function () {
        if (datePicker.value) {
            computeBtn.disabled = false;
        } else {
            computeBtn.disabled = true;
        }
    });

    // Update Lapse Page link
    const currentYear = new Date().getFullYear();
    lapseLink.textContent = `${currentYear} YTD`;
    lapseLink.href = 'lapse';

    if (lapseHeading) {
        lapseHeading.textContent = `${currentYear} YTD`;
    }

    // Compute button click event
    computeBtn.addEventListener('click', function () {
        const dateStr = datePicker.value;

        fetch('/compute', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ date: dateStr })
        })
        .then(response => response.json())
        .then(data => {
            const dayName = data.day_name;
            const dayOfYear = data.day_of_year;
            const daysRemaining = data.days_remaining;
            const isPast = data.is_past;
            const isToday = data.is_today;
            const isFuture = data.is_future;
            
            const dateObj = new Date(dateStr);
            const formattedDate = dateObj.toLocaleDateString(undefined, { year: 'numeric', month: 'long', day: 'numeric' });
            let message;

            if (isPast) {
                message = `${formattedDate} was on a ${dayName}. It was the ${dayOfYear} day of the year and there were ${daysRemaining} days remaining in ${dateObj.getFullYear()}.`;
            } else if (isToday) {
                message = `Alas, ${formattedDate} falls on this very day which is a ${dayName}. Today is the ${dayOfYear} day of this year and ${daysRemaining} days remain in ${dateObj.getFullYear()}.`;
            } else if (isFuture) {
                message = `${formattedDate} will be on a ${dayName}. It will be the ${dayOfYear} day of ${dateObj.getFullYear()} and there will be ${daysRemaining} days remaining in the year.`;
            }

            message += `<p>More about <a href="https://en.wikipedia.org/wiki/${dateObj.getMonth() + 1}_${dateObj.getDate()}" target="_blank">${dateObj.getMonth() + 1} ${dateObj.getDate()}</a> on Wikipedia.</p>`;

            resultDiv.innerHTML = message;
            resultDiv.classList.remove('hidden');
        });
    });
});
