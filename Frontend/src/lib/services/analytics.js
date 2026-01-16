import { fetchHealthData } from "$lib/API/AnalyticsAPI/HealthDataAPI";
import { fetchBreedData } from "$lib/API/AnalyticsAPI/BreedDataAPI";
import { fetchMilkYieldData } from "$lib/API/AnalyticsAPI/MilkYieldDataAPI";
import { fetchWaterData } from "$lib/API/AnalyticsAPI/WaterDataAPI";

export async function getHealthChartData() {
  return fetchHealthData();
}

export async function getBreedChartData() {
  return fetchBreedData();
}

export async function getMilkYieldChartData() {
  return fetchMilkYieldData();
}

export async function getWaterIntakeChartData() {
  return fetchWaterData();
}
