import { ChartComponent } from "../components/DisplayedDashboard/displayed-dashboard";
import { DataHandler } from "./data_handlers";
import { ExternalLibrary } from "./external_library_enum";

type ExpectedTableDataPayload = {
  columnNames: string[];
  rows: any[];
};

class TableDataHandler extends DataHandler {
  renderer: ExternalLibrary;
  type: string = "bar";
  ctx: any;

  constructor(
    component: ChartComponent,
    renderer: ExternalLibrary,
    ctx: any,
    parameters: any,
  ) {
    super(component, parameters);
    this.renderer = renderer;
    this.ctx = ctx;
  }

  getData(): ExpectedTableDataPayload | null {
    return null;
  }

  async processIntoTable() {
    const data = await this.getData();
    const columnNames = data.columnNames;
    let fields = columnNames.map((columnName) => {
      return columnName.split(" ").join("_").toLowerCase();
    });

    let rows = [];
    for (let i = 0; i < data.rows.length; i++) {
      let row = {};
      for (let j = 0; j < data.rows[i].length; j++) {
        row[fields[j]] = data.rows[i][j];
      }
      rows.push(row);
    }

    return {
      rows: rows,
      fields: fields,
      columnNames: columnNames,
    };
  }
}

class TableDataHandlerFrontend extends TableDataHandler {
  constructor(
    component: ChartComponent,
    renderer: ExternalLibrary,
    ctx: any,
    parameters: any = null,
  ) {
    super(component, renderer, ctx, parameters);
  }

  async getData(): ExpectedTableDataPayload {
    await setTimeout(() => {
      console.log("Emulating server");
    }, 2000);
    if (!this.getParameters()) {
      return {
        columnNames: ["Code", "Name", "Category", "Quantity", "Price"],
        rows: [
          ["R01", "Product 1", "Category 1", 10, 757],
          ["R02", "Product 2", "Category 2", 20, 123],
          ["R03", "Product 3", "Category 3", 30, 456],
          ["R04", "Product 4", "Category 4", 40, 789],
          ["R05", "Product 5", "Category 5", 50, 1011],
          ["R06", "Product 6", "Category 6", 60, 1213],
          ["R07", "Product 7", "Category 7", 70, 1415],
          ["R08", "Product 8", "Category 8", 80, 1617],
          ["R09", "Product 9", "Category 9", 90, 1819],
          ["R10", "Product 10", "Category 10", 100, 2021],
        ],
      };
    } else {
      return {
        columnNames: ["Code", "Name", "Category", "Quantity", "Price"],
        rows: [
          ["R01", "Product 1", "Category 1", 10, 757],
          ["R02", "Product 2", "Category 2", 20, 123],
          ["R03", "Product 3", "Category 3", 30, 456],
          ["R04", "Product 4", "Category 4", 40, 789],
        ],
      };
    }
  }
}

class TableDataHandlerBackend extends TableDataHandler {
  constructor(
    component: ChartComponent,
    renderer: ExternalLibrary,
    ctx: any,
    parameters: any = null,
  ) {
    super(component, renderer, ctx, parameters);
  }

  async getData(): ExpectedTableDataPayload {
    console.log(this.component);
    console.log(this.interpretDefaults(this.component.search_parameters));
    console.log(this.parameters);
    const component = this.component;
    switch (component.data_source_type) {
      case "API":
        try {
          const response = await fetch(component.data_source_path, {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              "X-Requested-With": "XMLHttpRequest",
            },
            body: JSON.stringify(
              this.parameters
                ? this.parameters
                : this.interpretDefaults(component.search_parameters),
            ),
          });
          const data = await response.json();
          console.log(data);
          return data.result;
        } catch (error) {
          console.error("Error fetching table data:", error);
        }
        break;
    }
  }
}

export class TableDataFactory {
  async getInstance(
    component: ChartComponent,
    context: any,
    parameters: any,
  ): DataHandler | void {
    if (import.meta.env.VITE_DASHBOARD_DATA_ENGINE === "frontend") {
      return new TableDataHandlerFrontend(
        component,
        ExternalLibrary.PrimeVue,
        context,
        parameters,
      );
    } else if (import.meta.env.VITE_DASHBOARD_DATA_ENGINE === "backend_odoo") {
      return new TableDataHandlerBackend(
        component,
        ExternalLibrary.PrimeVue,
        context,
        parameters,
      );
    }
  }
}
