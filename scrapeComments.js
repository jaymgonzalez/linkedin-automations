// Function to download data as a CSV file
function downloadCSV(csv, filename) {
  var csvFile
  var downloadLink

  // CSV file
  csvFile = new Blob([csv], { type: 'text/csv' })

  // Download link
  downloadLink = document.createElement('a')

  // File name
  downloadLink.download = filename

  // Create a link to the file
  downloadLink.href = window.URL.createObjectURL(csvFile)

  // Hide download link
  downloadLink.style.display = 'none'

  // Add the link to DOM
  document.body.appendChild(downloadLink)

  // Click download link
  downloadLink.click()
}

function extractDataAndDownloadCSV() {
  var usernames = document.querySelectorAll('.username') // Placeholder selector
  var userUrls = document.querySelectorAll('.userUrl') // Placeholder selector
  var comments = document.querySelectorAll('.comment') // Placeholder selector
  var csv = []

  // Header row
  csv.push('username,userUrl,comment')

  // Data rows
  for (let i = 0; i < usernames.length; i++) {
    var username = usernames[i].innerText || usernames[i].textContent
    var userUrl = userUrls[i].getAttribute('href')
    var comment = comments[i].innerText || comments[i].textContent

    // Escape commas and double quotes from the comment
    comment = comment.replace(/"/g, '""')
    if (comment.includes(',')) comment = `"${comment}"`

    csv.push(`${username},${userUrl},${comment}`)
  }

  // Download CSV
  downloadCSV(csv.join('\n'), 'data.csv')
}

// Run the function to extract data and download it as a CSV
extractDataAndDownloadCSV()
