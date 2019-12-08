/* remove notifications */
export function flashClose(): void {
  document.addEventListener("DOMContentLoaded", (): void => {

    function remove(target: Element): void {
      const enclose: (Element | null) = target.parentElement;
      if (!enclose) { return; }

      enclose.removeChild(target);
      if (enclose.children.length) { return; }

      const section: (Element | null) = enclose.parentElement;
      if (!section) { return; }

      const parent: (Element | null) = section.parentElement;
      if (!parent) { return; }

      parent.removeChild(section);
    }

    for (const delButton of document.querySelectorAll(".delete.click") as any) {
      delButton.addEventListener("click", function(this: Element): void {

         for (const selector of [".message", ".notification"]) {

          const target: (Element | null) = this.closest(selector);
          if (target) { remove(target); }

        }

      });
    }

  });
}
