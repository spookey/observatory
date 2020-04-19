import conf from "./settings";
import { colorizeSO } from "./colors";
import { drawCharts } from "./charts";
import { flashClose } from "./notifications";
import { momentTime } from "./moments";

conf.initialize();

colorizeSO();
drawCharts();
flashClose();
momentTime();
