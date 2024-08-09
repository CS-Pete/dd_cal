document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('date-form');
    const monthSelect = document.getElementById('month');
    const daySelect = document.getElementById('day');
    const yearInput = document.getElementById('year');
    const computeButton = document.getElementById('compute');
    const resultDiv = document.getElementById('result');
    const resultText = document.getElementById('result-text');
    const moreInfo = document.getElementById('more-info');

    const validateForm = () => {
        const month = monthSelect.value;
        const day = daySelect.value;
        const year = yearInput.value;
        computeButton.disabled = !(month && day && year);
    };

    monthSelect.addEventListener('change', validateForm);
    daySelect.addEventListener('change', validateForm);
    yearInput.addEventListener('input', validateForm);

    form.addEventListener('submit', function (e) {
        e.preventDefault();

        const month = monthSelect.value;
        const day = daySelect.value;
        const year = yearInput.value;

        fetch('/calculate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ month, day, year })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
            } else {
                resultDiv.classList.remove('hidden');

                let tenseText = '';
                if (data.tense === 'past') {
                    tenseText = `${data.month} ${data.day}, ${data.year} was on a ${data.day_of_week}. It was the ${data.day_of_year}th day of the year and there were ${data.days_remaining} days remained in ${data.year}.`;
                } else if (data.tense === 'present') {
                    tenseText = `Alas, ${data.month} ${data.day}, ${data.year} falls on this very day which is a ${data.day_of_week}. Today is the ${data.day_of_year}th day of this year and ${data.days_remaining} days remain in ${data.year}.`;
                } else {
                    tenseText = `${data.month} ${data.day}, ${data.year} will be on a ${data.day_of_week}. It will be the ${data.day_of_year}th day of ${data.year} and there will be ${data.days_remaining} days remaining in the year.`;
                }

                resultText.textContent = tenseText;
                moreInfo.innerHTML = `More about <a href="https://en.wikipedia.org/wiki/${data.month}_${data.day}" target="_blank">${data.month} ${data.day}</a>`;
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred. Please try again.');
        });
    });
});
