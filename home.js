(function () {
  var threadList = document.querySelector("[data-blog-thread-list]");
  if (!threadList) return;

  fetch("/blog/", { cache: "no-cache", credentials: "same-origin" })
    .then(function (response) {
      if (!response.ok) throw new Error("Blog page request failed");
      return response.text();
    })
    .then(function (source) {
      var blogPage = new DOMParser().parseFromString(source, "text/html");
      var threadPanels = blogPage.querySelectorAll(".thread-panel");
      var cards = document.createDocumentFragment();

      threadPanels.forEach(function (panel) {
        var title = panel.querySelector("h2");
        var summary = panel.querySelector(".thread-dek");
        if (!title || !summary) return;

        var card = document.createElement("article");
        card.className = "content-panel";

        var heading = document.createElement("h3");
        var headingLink = document.createElement("a");
        headingLink.href = panel.id ? "/blog/#" + panel.id : "/blog/";
        headingLink.textContent = title.textContent.trim();
        heading.appendChild(headingLink);

        var description = document.createElement("p");
        description.textContent = summary.textContent.trim();

        card.appendChild(heading);
        card.appendChild(description);

        var firstPublishedPost = panel.querySelector(".thread-parts a[href]");
        if (firstPublishedPost) {
          var postLink = document.createElement("a");
          postLink.className = "text-link";
          postLink.href = firstPublishedPost.getAttribute("href");
          postLink.textContent = firstPublishedPost.textContent.trim();
          card.appendChild(postLink);
        }

        cards.appendChild(card);
      });

      if (cards.childNodes.length > 0) threadList.replaceChildren(cards);
      threadList.setAttribute("aria-busy", "false");
    })
    .catch(function () {
      threadList.setAttribute("aria-busy", "false");
    });
})();
