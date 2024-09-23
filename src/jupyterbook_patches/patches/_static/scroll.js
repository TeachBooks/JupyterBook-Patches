// Keep track of the scroll position
const NAVIGATION_ELEMENT_CLASS = "bd-sidebar-primary";

document.addEventListener("DOMContentLoaded", () => {
  addEventListener("beforeunload", () => {
    let elements = document.getElementsByClassName(NAVIGATION_ELEMENT_CLASS);

    if (elements.length === 0) {
      console.warn("No sidebar found, cannot save scroll position");
      return;
    }

    localStorage.setItem("navigationScrollPosition", elements[0].scrollTop);
  });

  let elements = document.getElementsByClassName(NAVIGATION_ELEMENT_CLASS);

  if (elements.length === 0) {
    console.warn("No sidebar found, cannot restore scroll position");
    return;
  }

  let scrollPosition = localStorage.getItem("navigationScrollPosition");
  if (scrollPosition == null) {
    return;
  }

  // Convert scroll position into a positive number and apply it
  let parsedPosition = Math.abs(scrollPosition);
  console.debug(`Restoring scroll position to ${parsedPosition}`);
  elements[0].scrollTop = isNaN(parsedPosition) ? 0 : parsedPosition;
});
