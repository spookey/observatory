import axios from "axios";
import { colorizeSO } from "./colors";
import { doSettings } from "./settings";
import { drawCharts } from "./charts";
import { flashClose } from "./notifications";
import { momentTime } from "./moments";


(window as any).configure = doSettings;

colorizeSO();
drawCharts();
flashClose();
momentTime();
