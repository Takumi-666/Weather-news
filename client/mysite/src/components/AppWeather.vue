<template>
  <div class="homepage">
    <header class="header">
      <h1>Weather-news</h1>
      <div class="btn-container">
        <button @click="showModal">⍰</button>
      </div>
      <div id="app">
        <div id="mask" class="hidden" @click="hideModal"></div>
        <section id="modal" class="hidden">
          <p>
            このページは各地の天気予報を集めて表示しています。
            <br />
            <br />
            画面下に各地の天気のランキングもあります。是非見てね！
          </p>
        </section>
      </div>
    </header>
    <main class="main-content">
      <!-- 都市ごとにデータをグループ化 -->
      <div v-for="(city, index) in groupedData" :key="index">
        <h2>{{ translateCityName(city.city) }}</h2>
        <div class="weather-list">
          <div
            v-for="(weather, wIndex) in city.weatherList"
            :key="wIndex"
            class="weather-item"
          >
            <div class="weather-header">
              <img
                :src="getWeatherIconUrl(weather.icon_code)"
                alt="weather icon"
                class="weather-icon"
              />
              <span class="weather-date">{{ formatDate(weather.date) }}</span>
            </div>
            <div class="weather-details">
              <div class="weather-temperature">
                <span class="max-temp"
                  >最高 {{ weather.max_temp | roundUp }}°C</span
                >
                <span class="min-temp"
                  >最低 {{ weather.min_temp | roundUp }}°C</span
                >
              </div>
              <div class="weather-humidity">湿度: {{ weather.humidity }}％</div>
              <div class="weather-wind-speed">
                風速: {{ weather.wind_speed | roundUp }}mph
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
    <body>
      <div class="ranking-container">
        <div class="ranking-section">
          <h2>最低気温ランキング</h2>
          <table>
            <thead>
              <tr>
                <th>順位</th>
                <th>都市名</th>
                <th>日付</th>
                <th>最低気温 (°C)</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="item in calculateMinTemperatureRanking().slice(0, 5)"
                :key="item.rank"
              >
                <td>
                  {{ item.rank }}
                  <span class="rank-emoji">{{ item.emoji }}</span>
                </td>
                <td>{{ item.city }}</td>
                <td>{{ item.date }}</td>
                <td>{{ item.temperature }}°C</td>
              </tr>
            </tbody>
          </table>
        </div>
        <!-- 最高気温ランキング -->
        <div class="ranking-section">
          <h2>最高気温ランキング</h2>
          <table>
            <thead>
              <tr>
                <th>順位</th>
                <th>都市名</th>
                <th>日付</th>
                <th>最高気温 (°C)</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="item in calculateMaxTemperatureRanking().slice(0, 5)"
                :key="item.rank"
              >
                <td>
                  {{ item.rank }}
                  <span class="rank-emoji">{{ item.emoji }}</span>
                </td>
                <td>{{ item.city }}</td>
                <td>{{ item.date }}</td>
                <td>{{ item.temperature }}°C</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <div class="ranking-container">
        <!-- 湿度ランキング -->
        <div class="ranking-section">
          <h2>湿度ランキング</h2>
          <table>
            <thead>
              <tr>
                <th>順位</th>
                <th>都市名</th>
                <th>日付</th>
                <th>湿度 (%)</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="item in calculateHumidityRanking().slice(0, 5)"
                :key="item.rank"
              >
                <td>
                  {{ item.rank }}
                  <span class="rank-emoji">{{ item.emoji }}</span>
                </td>
                <td>{{ item.city }}</td>
                <td>{{ item.date }}</td>
                <td>{{ item.humidity }}%</td>
              </tr>
            </tbody>
          </table>
        </div>
        <!-- 風速ランキング -->
        <div class="ranking-section">
          <h2>風速ランキング</h2>
          <table>
            <thead>
              <tr>
                <th>順位</th>
                <th>都市名</th>
                <th>日付</th>
                <th>風速 (mph)</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="item in calculateWindSpeedRanking().slice(0, 5)"
                :key="item.rank"
              >
                <td>
                  {{ item.rank }}
                  <span class="rank-emoji">{{ item.emoji }}</span>
                </td>
                <td>{{ item.city }}</td>
                <td>{{ item.date }}</td>
                <td>{{ item.windSpeed }}mph</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </body>
  </div>
</template>

<script>
import axios from "axios";
import moment from "moment";

export default {
  data() {
    return {
      woeid: null, // 地域ID
      weatherList: [],
      cityName: "", // 都市名を格納
    };
  },
  methods: {
    formatDate(timestamp) {
      return moment.unix(timestamp).format("YYYY-MM-DD");
    },

    // 天気アイコンのURLを取得するメソッド
    getWeatherIconUrl(iconCode) {
      // OpenWeatherのアイコンURLのベースパス
      const baseUrl = "http://openweathermap.org/img/w/";
      // アイコンコードを使用してアイコンのURLを構築
      return `${baseUrl}${iconCode}.png`;
    },

    fetchData() {
      // DjangoのビューからOpenWeather APIデータを取得するエンドポイントを指定
      const weatherEndpoint = "http://localhost:8000/get_weather/";

      axios
        .get(weatherEndpoint)
        .then((response) => {
          // データを取得したら、コンソールにログを出力
          console.log("データを取得しました:", response.data);
          this.weatherList = response.data; // APIからのデータをweatherListに設定
        })
        .catch((error) => {
          // エラーが発生した場合、コンソールにエラーメッセージを出力
          console.error("データを取得できませんでした:", error);
        });
    },
    translateCityName(cityName) {
      const cityTranslation = {
        Niigata: "新潟",
        Tokyo: "東京",
        Osaka: "大阪",
        Sapporo: "札幌",
        Fukuoka: "福岡",
      };
      return cityTranslation[cityName] || cityName;
    },

    calculateMaxTemperatureRanking() {
      const sortedData = this.weatherList
        .slice()
        .sort((a, b) => b.max_temp - a.max_temp);
      const maxTempRanking = sortedData.map((item, index) => {
        return {
          rank: index + 1,
          date: this.formatDate(item.date),
          temperature: item.max_temp,
          emoji:
            index === 0 ? "🥇" : index === 1 ? "🥈" : index === 2 ? "🥉" : "",
          city: this.translateCityName(item.city), // 都市名を日本語に変換
        };
      });
      return maxTempRanking;
    },

    calculateMinTemperatureRanking() {
      const sortedData = this.weatherList
        .slice()
        .sort((a, b) => a.min_temp - b.min_temp);
      const minTempRanking = sortedData.map((item, index) => {
        return {
          rank: index + 1,
          date: this.formatDate(item.date),
          temperature: item.min_temp,
          emoji:
            index === 0 ? "🥇" : index === 1 ? "🥈" : index === 2 ? "🥉" : "",
          city: this.translateCityName(item.city), // 都市名を日本語に変換
        };
      });
      return minTempRanking;
    },

    calculateWindSpeedRanking() {
      const sortedData = this.weatherList
        .slice()
        .sort((a, b) => b.wind_speed - a.wind_speed);
      const windSpeedRanking = sortedData.map((item, index) => {
        return {
          rank: index + 1,
          date: this.formatDate(item.date),
          windSpeed: item.wind_speed,
          emoji:
            index === 0 ? "🥇" : index === 1 ? "🥈" : index === 2 ? "🥉" : "",
          city: this.translateCityName(item.city), // 都市名を日本語に変換
        };
      });
      return windSpeedRanking;
    },

    calculateHumidityRanking() {
      const sortedData = this.weatherList
        .slice()
        .sort((a, b) => b.humidity - a.humidity);
      const humidityRanking = sortedData.map((item, index) => {
        return {
          rank: index + 1,
          date: this.formatDate(item.date),
          humidity: item.humidity,
          emoji:
            index === 0 ? "🥇" : index === 1 ? "🥈" : index === 2 ? "🥉" : "",
          city: this.translateCityName(item.city), // 都市名を日本語に変換
        };
      });
      return humidityRanking;
    },
    showModal() {
      const mask = document.getElementById("mask");
      const modal = document.getElementById("modal");
      mask.classList.remove("hidden");
      modal.classList.remove("hidden");
    },
    hideModal() {
      const mask = document.getElementById("mask");
      const modal = document.getElementById("modal");
      mask.classList.add("hidden");
      modal.classList.add("hidden");
    },
  },
  computed: {
    // 都市ごとにデータをグループ化する計算プロパティ
    groupedData() {
      const grouped = {};
      this.weatherList.forEach((weather) => {
        if (!grouped[weather.city]) {
          grouped[weather.city] = {
            city: weather.city,
            weatherList: [],
          };
        }
        grouped[weather.city].weatherList.push(weather);
      });
      return Object.values(grouped);
    },
  },

  filters: {
    roundUp(value) {
      return Math.ceil(value);
    },
  },
  created() {
    // ページがロードされた後にデータを取得
    this.fetchData();
  },
};
</script>

<style scoped>
.homepage {
  font-family: Arial, sans-serif;
  background-color: #9af1eb;
  position: relative; /* 親要素を相対配置に設定 */
  overflow: hidden; /* オーバーフローを隠す */
}

.header {
  background-color: #007bff;
  color: white;
  text-align: center;
  padding: 1rem;
  position: relative; /* 相対配置に設定 */
}

.btn-container {
  position: absolute; /* 絶対配置に設定 */
  top: 10px; /* 上端からの位置を調整 */
  right: 10px; /* 右端からの位置を調整 */
}

button {
  width: 40px; /* ボタンの幅を調整 */
  height: 40px; /* ボタンの高さを調整 */
  font-size: 24px; /* ボタンのフォントサイズを調整 */
  font-weight: bold;
  cursor: pointer;
  border: none; /* ボーダーをなしに設定 */
  color: #ffffff; /* テキストの色を設定 */
}

button:hover {
  opacity: 0.7;
}

.hidden {
  display: none;
}

#mask {
  background: rgba(0, 0, 0, 0.7);
  position: fixed;
  top: 0;
  bottom: 0;
  right: 0;
  left: 0;
  z-index: 1;
}

#modal {
  background: #fff;
  width: 50%;
  padding: 24px;
  border-radius: 4px;
  color: red;
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
  margin: 0 auto;
  z-index: 2;
}

.hidden {
  display: none;
}

.main-content {
  padding: 1rem;
}
h2 {
  font-size: 1.5rem; /* フォントサイズを調整 */
  font-weight: bold; /* フォントの太さを調整 */
  text-decoration: underline; /* 下線を引く */
  margin-bottom: 0.5rem; /* 下側の余白を調整 */
  color: #333; /* テキストの色を設定 */
}
.weather-city {
  font-weight: bold;
  font-size: 18px;
  color: #333;
}

.weather-list {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
}

.weather-item {
  background-color: #fff;
  padding: 10px;
  width: calc(33.33% - 10px); /* 3列で表示 */
  margin-bottom: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.weather-header {
  display: flex;
  align-items: center;
}

.weather-icon {
  width: 32px;
  height: 32px;
  margin-right: 10px;
}

.weather-date {
  font-weight: bold;
}

.weather-state {
  font-weight: bold;
}

.weather-temperature {
  margin-top: 8px;
  font-size: 14px;
}

.max-temp {
  color: #ff6347; /* 最高気温のテキストカラーを設定 */
}

.min-temp {
  color: #1e90ff; /* 最低気温のテキストカラーを設定 */
}
.weather-wind-speed {
  font-size: 12px;
  margin-top: 4px;
  color: #777;
}
body {
  background-color: #9af1eb; /* ヘッダーの背景色を設定 */
  color: white;
  text-align: center;
  padding: 1rem;
}
/* ランキングコンテナ全体のスタイル */
.ranking-container {
  display: flex;
  justify-content: space-between;
}

/* 個別のランキングセクションのスタイル */
.ranking-section {
  width: 48%; /* 2つのセクションを均等に分割 */
  padding: 10px;
  border: 1px solid #100202;
}

/* ランキングタイトルのスタイル */
.ranking-section h2 {
  font-size: 1.5rem;
  margin-bottom: 10px;
}

.ranking-section table {
  border-collapse: collapse;
  width: 100%;
  margin-bottom: 20px;
  border: 2px solid #333; /* テーブル全体のボーダーを追加 */
}

.ranking-section th,
.ranking-section td {
  border: 2px solid #333; /* セルのボーダーを追加 */
  padding: 12px;
  text-align: center; /* セル内のテキストを中央揃えにする */
}

.ranking-section th {
  background-color: #333; /* ヘッダーの背景色を変更 */
  color: white; /* ヘッダーテキストの色を白に設定 */
  font-weight: bold;
}

.ranking-section td {
  background-color: #777272; /* セルの背景色を変更 */
}

/* ランキングの絵文字スタイル */
.rank-emoji {
  font-size: 1.2rem;
  margin-right: 4px;
  vertical-align: middle; /* 絵文字をテキストの中央に配置 */
}
</style>
