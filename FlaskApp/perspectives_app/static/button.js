document.querySelector('button').addEventListener('click', toggle)

function toggle(event) {
  if (document.getElementsByClassName('radar-chart').style.display == 'none') {
    event.target.innerText = 'Display Emoji Cloud'
    document.getElementsByClassName('radar-chart').style.display = ''
    document.getElementsByClassName('emoji-cloud').style.display = 'none'
  } else {
    event.target.innerText = 'Display Radar Chart'
    document.getElementsByClassName('radar-chart').style.display = 'none'
    document.getElementsByClassName('emoji-cloud').style.display = ''
  }
}