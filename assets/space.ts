import axios from "axios";
import { AxiosError } from "axios";
import { AxiosRequestConfig } from "axios";
import { AxiosResponse } from "axios";

import conf from "./settings";

class SpaceContent {
  private box: HTMLElement;

  private config: AxiosRequestConfig = {
    baseURL: conf.apiSpaceApiUrl,
    method: "get",
    responseType: "json",
    timeout: 10 * 1000,
  };

  constructor(
    box: HTMLElement,
  ) {
    this.box = box;
  }

  private set(content: object): void {
    for (const element of this.box.getElementsByTagName('code') as any) {
      if (element instanceof HTMLElement) {
        element.innerText = JSON.stringify(content, null, 2);
      }
    }
  }

  public fill(): void {
    axios.get("", this.config)
      .then((res: AxiosResponse): void => {
        this.set(res.data);
      })
      .catch((err: AxiosError): void => {
        this.set({error: err});
      })
  }
}

export const sApiHelper = (): void => {
  document.addEventListener("DOMContentLoaded", (): void => {
    const fill = (box: (HTMLElement | null)): void => {
      if (!box) { return; }
      new SpaceContent(box).fill();
    };

    fill(document.querySelector('#spaceapi-rendered'));
  });
}
