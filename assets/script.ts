import axios from "axios";
import Chart from "chart.js";
import { colorizeSO } from "./colors";
import { doSettings } from "./settings";
import { flashClose } from "./notifications";
import { momentTime } from "./moments";

(window as any).configure = doSettings;

colorizeSO();
flashClose();
momentTime();
