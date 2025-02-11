class UserInfo {
  utc_time_diff: number;

  constructor(utc_time_diff: number) {
    this.utc_time_diff = utc_time_diff;
  }

  getUTCTimeDiff() {
return this.utc_time_diff;
  }

  setUTCTimeDiff(time_uff: number) {
    this.utc_time_diff = time_uff;
  }
}

async function getDataFrontend(): Promise<any> {
  try {
    console.log("Fetching data...");

    const response = await (async () => {
      return new Promise((resolve, reject) => {
        setTimeout(() => {
          if (Math.random() > 0.2) {
            // 80% success rate
            resolve({ utc_diff: -6 });
          } else {
            reject(new Error("Network error!"));
          }
        }, 3000);
      });
    })();
    return response; // Return the fetched data
  } catch (error) {
    console.error("Error fetching data:", error.message);
    return { error: error.message }; // Return error object
  }
}

async function getDataBackend(): Promise<any> {
  try {
    const response = await fetch(`/wb_data/get_user_info`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-Requested-With": "XMLHttpRequest",
      },
      body: JSON.stringify({}),
    });
    const data = await response.json();
    return data.result;
  } catch (error) {
    console.error(error);
  }
}

class UserInfoFactory {
  async getInstance(): Promise<UserInfo> {
    let data = null;
    switch (import.meta.env.VITE_DASHBOARD_DATA_ENGINE) {
      case "frontend":
        data = await getDataFrontend();
        break;
      case "backend_odoo":
        data = await getDataBackend();
        break;
    }

    let info = new UserInfo(data.utc_diff);
    return info;
  }
}


export const userInfoState = {
  userInfo: null 
}

export const userInfoGetters = {
  getUserInfo: async (state) => {
    let userInfoObj = new UserInfoFactory()
    state.userInfo = await userInfoObj.getInstance()
    console.log("======================0")
    console.log(state.userInfo)
    console.log("======================0")
    return state.userInfo
  }
}


