import axios from "axios";
import Chart from "chart.js";
import { colorizeSO } from "./colors";
import { flashClose } from "./notifications";
import { momentTime } from "./moments";

colorizeSO();
flashClose();
momentTime();
