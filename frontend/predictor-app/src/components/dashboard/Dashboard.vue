<template>
  <div class="dashboard-container">
    <div v-if="summary" class="kpi-grid">
      <div class="card">
        <h3>Total Survey Records</h3>
        <p class="stat-number">{{ summary.total_cases_analyzed.toLocaleString() }}</p>
      </div>
      <div class="card alert-card">
        <h3>Average Stunting Prevalence</h3>
        <p class="stat-number">{{ summary.average_risk_rate }}%</p>
      </div>
    </div>

    <div class="charts-grid">
      <div class="chart-card">
        <h3>Prevalence Rate by Province (%)</h3>
        <apexchart 
          type="bar" 
          height="350" 
          :options="provinceChartOptions" 
          :series="provinceSeries"
        ></apexchart>
      </div>

      <div class="chart-card">
        <h3>Prevalence Rate by Factor / Wealth Tier (%)</h3>
        <apexchart 
          type="line" 
          height="350" 
          :options="wealthChartOptions" 
          :series="wealthSeries"
        ></apexchart>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const summary = ref(null);
const provinceSeries = ref([]);
const provinceChartOptions = ref({ 
  chart: { id: 'province-bar', toolbar: { show: false } }, 
  xaxis: { categories: [] },
  colors: ['#42b883']
});

const wealthSeries = ref([]);
const wealthChartOptions = ref({ 
  chart: { id: 'wealth-line', toolbar: { show: false } }, 
  xaxis: { categories: [] },
  colors: ['#e056fd']
});

// Human-readable labels mapping for your dataset codes
const provinceLabels = {
  "0": "Balochistan",
  "1": "Balochistan",
  "2": "Sindh",
  "3": "KPK",
  "0.0": "Balochistan",
  "1.0": "Balochistan",
  "2.0": "Sindh",
  "3.0": "KPK"
};

// Fallback handles generic indices cleanly if wealth_index was replaced by housing_quality
const wealthLabels = {
  "1": "Poorest / Tier 1",
  "2": "Poorer / Tier 2",
  "3": "Middle / Tier 3",
  "4": "Richer / Tier 4",
  "5": "Richest / Tier 5",
  "1.0": "Poorest / Tier 1",
  "2.0": "Poorer / Tier 2",
  "3.0": "Middle / Tier 3",
  "4.0": "Richer / Tier 4",
  "5.0": "Richest / Tier 5"
};

onMounted(async () => {
  try {
    const apiUrl = import.meta.env.VITE_API_URL || '/api'
    const response = await fetch(`${apiUrl}/dashboard-stats`);
    const json = await response.json();
    
    if (json.status === 'success') {
      summary.value = json.summary;
      
      // Map raw numeric keys to geographic text names safely
      const dynamicProvinceCategories = json.charts.provinces.labels.map(key => provinceLabels[key] || `Region ${key}`);
      const dynamicWealthCategories = json.charts.wealthTiers.labels.map(key => wealthLabels[key] || `Index ${key}`);
      
      // Load Province Data Breakdown
      provinceSeries.value = [{ name: 'Stunting Prevalence', data: json.charts.provinces.data }];
      provinceChartOptions.value = { ...provinceChartOptions.value, xaxis: { categories: dynamicProvinceCategories } };
      
      // Load Wealth Tier / Factor Data Breakdown
      wealthSeries.value = [{ name: 'Stunting Prevalence', data: json.charts.wealthTiers.data }];
      wealthChartOptions.value = { ...wealthChartOptions.value, xaxis: { categories: dynamicWealthCategories } };
    }
  } catch (error) {
    console.error("Error pulling pipeline dashboard metrics:", error);
  }
});
</script>

<style scoped>
.dashboard-container {
  padding: 1rem 2rem;
  max-width: 1200px;
  margin: 0 auto;
}
.kpi-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}
.card {
  padding: 1.5rem;
  background: #fdfdfd; /* Fallback to a clear background */
  border: 5px solid transparent;
  border-radius: 6px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}
.alert-card {
  border-left-color: #ff2b2bda;
}
.stat-number {
  font-size: 2rem;
  font-weight: bold;
  margin: 0;
  color: #2c3e50; /* Hardcoded safe color */
}
.charts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(450px, 1fr));
  gap: 2rem;
}
.chart-card {
  background: #ffffff; /* Fallback safe bright white backgrounds */
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  border: 1px solid #eeeeee;
}
h3 {
  margin-top: 0;
  color: #7f8c8d; /* Safe grey colors */
  font-size: 1rem;
  margin-bottom: 1rem;
}
</style>