<script>
import './Form.css'
</script>

<template>
  <form>
    <div class="input-box">
        <label>Child Age (in months)</label>
        <input type="number" required>
    </div>
    <div class="divider-line"></div>
    <div class="input-box">
        <label>Mother's Education</label>
        <p>On a scale of 1 - 5</p>
        <input type="number" required>
    </div>
    <div class="divider-line"></div>
    <div class="input-box">
        <label>Wealth Index</label>
        <p>On a scale of 1 - 5</p>
        <input type="number" required>
    </div>
    <div class="divider-line"></div>
    <div class="input-box">
        <label>District Type</label>
        <p>Urban or rural?</p>
        <select id="district_type" name="district_type">
            <option value=0>Rural</option>
            <option value=1>Urban</option>
        </select>
    </div>
    <div class="divider-line"></div>
    <div class="input-box">
        <label>Province</label>
        <select id="province" name="province">
            <option value=0>Sindh</option>
            <option value=1>Balochistan</option>
            <option value=2>KPK</option>
        </select>
    </div>
    <div class="divider-space"></div>
    <button type="submit">Make Prediction</button>
  </form>
</template>