const fs = require("fs");
const data = fs.readFileSync("menu.json", { encoding: "utf8" });
const json = JSON.parse(data);
const menu_month_calendar = json.data.menu_month_calendar;
const resObj = { title: json.data.menu_info.menu_title, menu_days: [] };
for (menu of menu_month_calendar) {
  const date = menu.day;
  const setting = JSON.parse(menu.setting);
  const items = setting.current_display;
  let category = "";
  const myItems = [];
  for (item of items) {
    if (item.type === "category") {
      const categoryName = item.name;
      if (categoryName != category) {
        category = categoryName;
      }
    } else if (item.type === "recipe") {
      myItems.push({
        category: category,
        name: item.name,
        weight: item.weight,
      });
    }
  }
  const day_menu = { date, items: myItems };
  resObj.menu_days.push(day_menu);
}
console.log(JSON.stringify(resObj, null, 2));
