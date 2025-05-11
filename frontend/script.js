document.getElementById('askButton').addEventListener('click', async () => {
    const questionInput = document.getElementById('questionInput').value;
    const responseDiv = document.getElementById('response');

    // Clear previous response
    responseDiv.innerHTML = '';

    if (!questionInput) {
        responseDiv.innerHTML = '<p style="color: red;">Please enter a question.</p>';
        return;
    }

    try {
        // Send the question to the backend
        const response = await fetch('http://127.0.0.1:5000/ask', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ query: questionInput }),
        });

        if (response.ok) {
            const data = await response.json();
            if (data.answers && data.answers.length > 0) {
                responseDiv.innerHTML = data.answers
                    .map(
                        (answer) =>
                            `<div><strong>Q:</strong> ${answer.question}<br><strong>A:</strong> ${answer.answer}</div>`
                    )
                    .join('<hr>');
            } else {
                responseDiv.innerHTML = '<p>No relevant answers found.</p>';
            }
        } else {
            const errorData = await response.json();
            responseDiv.innerHTML = `<p style="color: red;">Error: ${errorData.message || 'Something went wrong.'}</p>`;
        }
    } catch (error) {
        responseDiv.innerHTML = `<p style="color: red;">Error: ${error.message}</p>`;
    }
});