;(async function () {
  const name = document.querySelector(
    '.pv-text-details__about-this-profile-entrypoint'
  ).innerText
  const kleo = document.querySelector('#kleo').shadowRoot
  let allData = []
  let processedIndices = new Set() // Set to keep track of processed indices

  const totalPosts = () => {
    const postElement = Array.from(
      kleo.querySelectorAll('[id*="headlessui-listbox-button"]')
    ).find((el) => el.textContent.includes('Posts')).innerText

    console.log('postElement: ', postElement)
    const totalPosts = parseInt(postElement.match(/\((\d+)\)/)[1])
    return totalPosts
  }

  const getEngagement = (element) => {
    const elements = element.querySelectorAll('span.text-low-emphasis-light')

    return elements[elements.length - 1].innerText.match(/(\d+)/g)
  }

  // const totalNumberOfItems = 200
  const totalNumberOfItems = totalPosts()

  console.log('Total number of posts: ', totalNumberOfItems)

  async function collectData() {
    const elements = kleo.querySelectorAll('[data-index]')
    for (let element of elements) {
      const dataIndex = parseInt(element.getAttribute('data-index'))
      // Example: Storing the innerText of each element// Only process if dataIndex has not been processed before
      if (!processedIndices.has(dataIndex)) {
        const engagement = getEngagement(element)
        // console.log('engagement: ', engagement)

        allData.push({
          index: dataIndex,
          type: element.querySelector('span.text-xs.font-medium.rounded-md')
            ?.innerText,
          postUrl: element
            .querySelector('a.text-linkedin-blue')
            ?.getAttribute('href'),
          imageUrl: element
            .querySelector('img.object-cover')
            ?.getAttribute('src'),
          pusblishDate: element.querySelector(
            'span.inline-flex.items-center.gap-x-1.text-low-emphasis-light'
          )?.innerText,
          reactions: parseInt(
            element.querySelector('span.-ml-1\\.5.text-low-emphasis-light')
              ?.innerText
          ),
          comments: parseInt(engagement[0]) || null,
          shares: parseInt(engagement[1]) || null,
          content: element.querySelector(
            '.relative.text-sm.mt-3.overflow-hidden'
          ).innerText,
        })
        processedIndices.add(dataIndex)
      }
    }
    if (allData.length < totalNumberOfItems - 1) {
      console.log(allData.length, totalNumberOfItems)
      elements[elements.length - 1].scrollIntoView()
      await new Promise((resolve) => setTimeout(resolve, 1000)) // Wait for any lazy-loaded elements
      return collectData() // Recursive call to check for more elements
    }
  }

  await collectData()

  const blob = new Blob([JSON.stringify(allData, null, 2)], {
    type: 'application/json',
  })
  const a = document.createElement('a')
  a.href = URL.createObjectURL(blob)
  a.download = `${name.replaceAll(' ', '-')}.json`
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
})()
