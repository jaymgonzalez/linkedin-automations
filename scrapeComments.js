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

async function delay(time) {
  return new Promise(function (resolve) {
    setTimeout(resolve, time)
  })
}

// Function to load more comments
async function loadMoreComments() {
  for (let i = 0; i < 3; i++) {
    var loadMoreCommentsButton = document.querySelector(
      '.comments-comments-list__load-more-comments-button'
    )
    await simulateMouseScrollToEnd()
    loadMoreCommentsButton.click()
    console.log('Clicked to load more comments...')
    await delay(5000)
    console.log('Loading more comments...')
  }

  console.log('Finished loading comments.')
}

function easeOutQuad(t) {
  return t * (2 - t)
}

async function simulateMouseScrollToEnd(duration = 1500, maxDuration = 30000) {
  let start = window.scrollY
  let currentTime = 0
  const increment = 50
  let timeoutReached = false

  // Set a timeout to mark when 30 seconds have passed
  setTimeout(() => {
    timeoutReached = true
  }, maxDuration)

  function animateScroll() {
    if (timeoutReached) {
      return
    }

    let documentHeight = Math.max(
      document.body.scrollHeight,
      document.documentElement.scrollHeight,
      document.documentElement.offsetHeight
    )
    let windowHeight = window.innerHeight
    let destination = documentHeight - windowHeight
    let change = destination - start

    currentTime += increment
    let val = easeOutQuad(currentTime / duration)
    window.scrollTo(0, start + change * val)

    if (window.scrollY < destination && currentTime < duration) {
      setTimeout(animateScroll, increment)
    } else if (window.scrollY < destination) {
      // If we haven't reached the new bottom, extend the duration slightly
      currentTime = 0 // Reset currentTime to allow the scroll to adjust to new content
      start = window.scrollY // Update start to current position
      setTimeout(animateScroll, increment)
    }
  }

  animateScroll()
}

function getUserName() {
  return document.querySelector(
    '.update-components-actor__container .update-components-actor__name .visually-hidden'
  ).innerText
}

function getHook() {
  return document
    .querySelector('.feed-shared-update-v2__description-wrapper')
    .innerText.split('\n')[0]
    .replaceAll(' ', '-')
}

async function extractDataAndDownloadCSV() {
  await loadMoreComments()

  var post = document.querySelector(
    '.feed-shared-update-v2__description-wrapper'
  ).innerText

  var commentContainer = document.querySelector(
    '.feed-shared-update-v2__comments-container'
  )

  var comments = commentContainer.querySelectorAll(
    '.comments-comment-item.comments-comments-list__comment-item'
  )

  var csv = []
  // Header row
  csv.push('fullName,n,c')

  // for (let i = 0; i < 4; i++) {
  for (let i = 0; i < comments.length; i++) {
    var username = comments[i]
      .querySelectorAll('.comments-post-meta a')[1]
      .innerText.split('\n')[0]
    var commentText = comments[i].querySelector(
      '.comments-comment-item-content-body'
    ).innerText

    // Escape commas and double quotes from the comment
    commentText = commentText.replace(/,/g, ';')
    commentText = commentText.replace(/\n/g, ' ')
    commentText = commentText.replace(/"/g, '')
    commentText = commentText.replace(getUserName(), '')

    username = username.replace(/,/g, '')

    csv.push(`${username},${username.split(' ')[0]},${commentText}`)
  }
  // csv.push(post)

  var filename = `${getUserName()}_${getHook()}`
  // Download CSV
  downloadCSV(csv.join('\n'), `${filename}.csv`)
}

// Run the function to extract data and download it as a CSV
extractDataAndDownloadCSV()
