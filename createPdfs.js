const arr = $json.content.split('\n\n')

const title = arr[0].split('\n')[0]
const subtitle = arr[0].split('\n')[1]
const takeaway = arr[arr.length - 1].replace(/\n$/, '')
const slides = arr.slice(1, -1)
const takeawayTitle = takeaway.split('\n')[0]
const takeawaySubtitle = takeaway.split('\n')[1]

const modifiedSlides = slides.map((slide) => {
  const parts = slide.split('\n')

  const number = parts[0]
  const title = parts[1]
  const subtitle = parts.slice(2).join('\n')

  return {
    template_uuid: 'v9wiu2nkgv2ao',
    layers: {
      number: { text: number },
      title: { text: title },
      subtitle: { text: subtitle },
    },
  }
})

const result = {
  pages: [
    {
      template_uuid: 'gxoysgq4tjkdh',
      layers: {
        title: {
          text: title,
        },
        subtitle: {
          text: subtitle,
        },
      },
    },
    ...modifiedSlides,
    {
      template_uuid: 'gpzptpw6kmwgm',
      layers: {
        title: {
          text: takeawayTitle,
        },
        subtitle: {
          text: takeawaySubtitle,
        },
      },
    },
  ],
}

return result
