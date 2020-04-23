/* make dropdown menus clickable */
export function dropToggle(): void {
  document.addEventListener("DOMContentLoaded", (): void => {
    const ACT: string = "is-active";

    function register(dropdown: HTMLElement): void {
      for (const trigger of dropdown.getElementsByClassName("dropdown-trigger") as any) {
        trigger.addEventListener("click", (): void => {
          dropdown.classList.toggle(ACT);
        });
      }
    }

    for (const dropdown of document.getElementsByClassName("dropdown") as any) {
      register(dropdown);
    }
  });
}
