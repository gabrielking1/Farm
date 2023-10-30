;(function () {
  const modal = new bootstrap.Modal(document.getElementById("modal"))

  htmx.on("htmx:afterSwap", (e) => {
    // Response targeting #exampleModal => show the modal
    if (e.detail.target.id == "exampleModal") {
      modal.show()
    }
  })

  htmx.on("htmx:beforeSwap", (e) => {
    // Empty response targeting #exampleModal => hide the modal
    if (e.detail.target.id == "exampleModal" && !e.detail.xhr.response) {
      modal.hide()
      e.detail.shouldSwap = false
    }
  })

  // Remove exampleModal content after hiding
  htmx.on("hidden.bs.modal", () => {
    document.getElementById("exampleModal").innerHTML = ""
  })
})()
