import xml.etree.ElementTree as ET

def parse_topic(topic_element, topic_id):
    """Recursively parse XML topic elements and convert them to HTML list items."""
    txt = topic_element.attrib.get('txt', '')
    url = 'resources/' + topic_element.attrib.get('url', '')

    # Generate HTML for the current topic with a unique ID for collapsing
    html = f'<li id="topic-{topic_id}" class="topic-item"><a target="content" href="{url}">{txt}</a>'

    # Check if the current topic has nested topics
    subtopics = topic_element.findall('topic')
    if subtopics:
        html += f' <button onclick="toggleSubtopics(\'subtopics-{topic_id}\')">[+]</button>'
        html += f'<ul id="subtopics-{topic_id}" style="display:none;" class="subtopics">'
        subtopic_id = 1
        for subtopic in subtopics:
            html += parse_topic(subtopic, f'{topic_id}-{subtopic_id}')
            subtopic_id += 1
        html += '</ul>'

    html += '</li>'
    return html

def generate_html_index(xml_file):
    """Parse the XML file and generate an HTML index."""
    # Parse the XML file
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Generate the HTML for the entire document
    html = '''
<html>
<head>
<style>
  body {
    font-family: Arial, sans-serif;
  }
  ul {
    list-style-type: none;
  }
  li {
    margin: 5px 0;
  }
  .search-box {
    margin-bottom: 20px;
  }
  .topic-item {
    display: block;
  }
  .subtopics {
    display: none;
  }
  .highlight {
    background-color: yellow;
  }
</style>
<script>
  function toggleSubtopics(id) {
    var subtopics = document.getElementById(id);
    if (subtopics.style.display === "none") {
      subtopics.style.display = "block";
    } else {
      subtopics.style.display = "none";
    }
  }

  function highlightMatch(text, filter) {
    var startIndex = text.toUpperCase().indexOf(filter);
    if (startIndex === -1) {
      return text;
    }
    var endIndex = startIndex + filter.length;
    return text.substring(0, startIndex) +
           '<span class="highlight">' + text.substring(startIndex, endIndex) + '</span>' +
           text.substring(endIndex);
  }

  function searchTopics() {
    var input, filter, ul, li;
    input = document.getElementById("searchInput");
    filter = input.value.toUpperCase();
    ul = document.getElementById("topicList");
    li = ul.getElementsByTagName("li");

    function searchAndToggle(li) {
      var a = li.getElementsByTagName("a")[0];
      var txtValue = a.textContent || a.innerText;
      if (filter) {
        var f = highlightMatch(txtValue, filter);
        if (a.innerHTML != f) {
            a.innerHTML = f;
        }
      }
      if (txtValue.toUpperCase().indexOf(filter) > -1) {
        li.style.display = "";
        return true;
      } else {
        var subtopics = li.getElementsByTagName("ul");
        var match = false;
        for (var i = 0; i < subtopics.length; i++) {
          var sublis = subtopics[i].getElementsByTagName("li");
          for (var j = 0; j < sublis.length; j++) {
            if (searchAndToggle(sublis[j])) {
              match = true;
            }
          }
          subtopics[i].style.display = match ? "block" : "none";
        }
        li.style.display = match ? "" : "none";

        return match;
      }
    }

    for (var i = 0; i < li.length; i++) {
      searchAndToggle(li[i]);
    }

    if (!filter) {
      resetTopics();
    }
  }

  function resetTopics() {
    var ul = document.getElementById("topicList");
    var li = ul.getElementsByTagName("li");
    for (var i = 0; i < li.length; i++) {
      li[i].style.display = "";
      var a = li[i].getElementsByTagName("a")[0];
      var txtValue = a.textContent || a.innerText;
      a.innerHTML = txtValue;
      var subtopics = li[i].getElementsByTagName("ul");
      for (var j = 0; j < subtopics.length; j++) {
        subtopics[j].style.display = "none";
      }
    }
  }
</script>
</head>
<body>
<div class="search-box">
  <input type="text" id="searchInput" onkeyup="searchTopics()" placeholder="Search topics...">
</div>
<ul id="topicList">
'''
    topic_id = 1
    for topic in root.findall('topic'):
        html += parse_topic(topic, topic_id)
        topic_id += 1

    html += '''
</ul>
</body>
</html>
'''
    return html

if __name__ == "__main__":
    xml_file = 'resources/navi.xml'  # Path to the XML file
    html_index = generate_html_index(xml_file)

    # Output the generated HTML to a file
    with open('toc.html', 'w', encoding='utf-8') as f:
        f.write(html_index)

    print("HTML index generated and saved to toc.html")

