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

// Function to load more comments
function loadMoreComments() {
  var loadMoreCommentsButton = document.querySelector(
    '.comments-comments-list__load-more-comments-button'
  )
  for (let i = 0; i < 5; i++) {
    simulateMouseScrollToEnd()
    loadMoreCommentsButton.click()
    setTimeout(() => {
      console.log('Loading more comments...')
    }, 3000)
  }
}

function easeOutQuad(t) {
  return t * (2 - t)
}

function simulateMouseScrollToEnd(duration = 2000) {
  let start = window.pageYOffset
  let end = document.body.offsetHeight - window.innerHeight
  let change = end - start
  let currentTime = 0
  const increment = 20

  function animateScroll() {
    currentTime += increment
    let val = easeOutQuad(currentTime / duration)
    window.scrollTo(0, start + change * val)
    if (currentTime < duration) {
      setTimeout(animateScroll, increment)
    }
  }

  animateScroll()
}

function extractDataAndDownloadCSV() {
  loadMoreComments()

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
