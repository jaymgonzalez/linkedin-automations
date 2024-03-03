const main = function () {
  const $json = {
    documentId: '1yJWVExHUVaqg793mt15S8BQ5L_Uqto3xVbUZzaUz-44',
    content:
      'This is the title\n\n1\nPara hacer bien el amor\nHay q venir la sur\n\n2\nSi tu abuela no te quier\nCocina\nportate bien\nLlevale comida\n\nThat’s i\n',
  }

  const arr = $json.content.split('\n\n')

  const title = arr[0].split('\n')[0]
  const subtitle = arr[0].split('\n')[1]
  const takeaway = arr[arr.length - 1].replace(/\n$/, '')
  const slides = arr.slice(1, -1)

  console.log(arr)

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
            text: takeaway,
          },
        },
      },
    ],
  }

  return result
}

console.log(main())
