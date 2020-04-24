/* make dropdown menus clickable */
export function dropToggle(): void {
  document.addEventListener("DOMContentLoaded", (): void => {
    const ACT: string = "is-active";
    const dropdowns: HTMLCollection = document.getElementsByClassName("dropdown");

    for (const dropdown of dropdowns as any) {
      dropdown.addEventListener("click", (event: Event): void => {
        event.stopPropagation();
        dropdown.classList.toggle(ACT);
      });
    }

    document.body.addEventListener("click", (): void => {
      for (const dropdown of dropdowns as any) {
        dropdown.classList.remove(ACT);
      }
    });
  });
}
