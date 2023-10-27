<template #event="{ event }">
  <div>
    <v-sheet tile height="6vh" color="grey lighten-3" class="d-flex align-center">
      <v-btn outlined small class="ma-4" @click="setToday">
        今日
      </v-btn>
      <v-btn icon @click="$refs.calendar.prev()">
        <v-icon>mdi-chevron-left</v-icon>
      </v-btn>
      <v-btn icon @click="$refs.calendar.next()">
        <v-icon>mdi-chevron-right</v-icon>
      </v-btn>
      <v-toolbar-title>{{ title }}</v-toolbar-title>
    </v-sheet>
    <!-- イベント名（ここでは天気情報）を表示 -->
    <strong>{{ event.name }}</strong><br>
    <!-- 天気情報を表示 -->
    <span>{{ event.description }}</span>
    <v-sheet height="94vh">
      <v-calendar
        ref="calendar"
        v-model="value"
        type="type"
        :events="events"
        :event-color="getEventColor"
        locale="ja-jp"
        :day-format="(timestamp) => new Date(timestamp.date).getDate()"
        :month-format="(timestamp) => new Date(timestamp.date).getMonth() + 1 + ' /'"
        @click:event="showEvent"
        @click:date="viewDay"
      ></v-calendar>
    </v-sheet>
  </div>
</template>

<script>
import moment from 'moment';
import axios from 'axios';

export default {
  data: () => ({
    type: '4day',
    value: moment().format('yyyy-MM-DD'),
    weatherData: [], // 3時間ごとの天気情報を格納するデータプロパティを追加
    events: [],
  }),
  computed: {
    title() {
      return moment(this.value).format('yyyy年 M月');
    },
  },
  mounted() {
    // DjangoのAPIエンドポイントにアクセスして天気情報を取得
    axios.get('http://localhost:8000/get_weather/')
      .then((response) => {
        this.weatherData = response.data;
        this.getEvents(); // カレンダーのイベント情報を取得
      })
      .catch((error) => {
        console.error('天気情報の取得に失敗しました', error);
      });
  },
  methods: {
    setToday() {
      this.value = moment().format('yyyy-MM-DD');
    },
    showEvent({ event }) {
      alert(`clicked ${event.name}`);
    },
    viewDay({ date }) {
      alert(`date: ${date}`);
    },
    getEvents() {
      // カレンダーのイベント情報を設定
      const events = this.weatherData.map((data) => {
        return {
          name: '天気情報',
          description: data.description, // 天気の説明を使用
          start: moment.unix(data.timestamp), // タイムスタンプを使用
          end: moment.unix(data.timestamp),
          color: 'blue', // 任意の色を指定
        };
      });

      this.events = events;
    },
    getEventColor(event) {
      return event.color;
    },
  },
};
</script>
