import { fetchHealthData } from "$lib/API/AnalyticsAPI/HealthDataAPI";
import { fetchBreedData } from "$lib/API/AnalyticsAPI/BreedDataAPI";
import { fetchMilkYieldData } from "$lib/API/AnalyticsAPI/MilkYieldDataAPI";
import { fetchWaterData } from "$lib/API/AnalyticsAPI/WaterDataAPI";

// --------------------
// Health (Donut)
// --------------------
export async function getHealthChartData() {
  const res = await fetchHealthData();

  return res.labels.map((label, i) => ({
    group: label,
    value: res.series[i]
  }));
}

// --------------------
// Breed (Donut)
// --------------------
export async function getBreedChartData() {
  const res = await fetchBreedData();

  return res.labels.map((label, i) => ({
    group: label,
    value: res.series[i]
  }));
}

// --------------------
// Milk Yield (Bar / Time Series)
// --------------------
export async function getMilkYieldChartData() {
  const res = await fetchMilkYieldData();

  return res.labels.map((day, i) => ({
    group: "Milk Yield",
    key: day,
    value: res.series[i]
  }));
}

// --------------------
// Water Intake (Bar)
// --------------------
export async function getWaterIntakeChartData() {
  const res = await fetchWaterData();

  return res.labels.map((label, i) => ({
    group: label,
    value: res.series[i]
  }));
}
