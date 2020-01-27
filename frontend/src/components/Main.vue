<template>
  <div class="pa-10">
    <v-data-table
      :headers="headers"
      :items="logs"
      :options.sync="options"
      :server-items-length="totalLogs"
      :loading="loading"
      :footer-props="{
        itemsPerPageOptions: [10, 20, 50]
      }"
      
    >
      <template v-slot:top>
        <v-row>
          <v-col cols="2">
            <v-select
              :items="filterFields"
              label="Search field"
              v-model="filterField"
              outlined
            ></v-select>
          </v-col>
          <v-col cols="6">
            <v-text-field
              v-if='filterField != "http_method"'
              v-model="filterValue"
              label="Search text"
              :width="100"
              outlined
            ></v-text-field>
            <v-select
              v-if='filterField == "http_method"'
              :items="httpMethods"
              label="Method"
              v-model="httpMethod"
              outlined
            ></v-select>
          </v-col>
          <v-col cols="4">
            <v-btn @click="getData" x-large>Search</v-btn>
          </v-col>
        </v-row>
      </template>
    </v-data-table>
    <br>
    Unique IPs: {{ uniqueIP }} <br>
    Total content length: {{ totalLength }} <br>
    <div v-if="loadingStatData">Loading stat data ....</div>
    <br>
    <StatTable :data="statData" v-if="statData.length" />
  </div>
</template>


<script>
import StatTable from './StatTable'

export default {
  name: "Main",
  components: {StatTable},
  data: () => ({
    filterFields: [
      {
        text: "IP Address",
        value: "ip_address"
      },
      {
        text: "HTTP Method",
        value: "http_method"
      },
      {
        text: "URI",
        value: "uri"
      },
      {
        text: "User Agent",
        value: "uset_agent"
      },
      {
        text: "Referer",
        value: "referer"
      }
    ],
    httpMethods: 'GET HEAD POST PUT DELETE CONNECT OPTIONS TRACE PATCH'.split(' '),
    httpMethod: '',
    filterField: '',
    filterValue: '',
    statData: [],
    loadingStatData: false,
    totalLogs: 0,
    logs: [],
    loading: true,
    options: {},
    totalLength: 0,
     uniqueIP: 0,
    headers: [
      { text: "IP Address", value: "ip_address" },
      { text: "Timestamp", value: "timestamp" },
      { text: "HTTP Method", value: "http_method" },
      { text: "URI", value: "uri" },
      { text: "Status Code", value: "status_code" },
      { text: "Length", value: "content_length" },
      { text: "User Agent", value: "user_agent" },
      { text: "Referer", value: "referer" }
    ]
  }),
  methods: {
    async getData() {
      this.loading = true;

      var params = new URLSearchParams();
      if (this.options.itemsPerPage)
        params.set("page_size", this.options.itemsPerPage);
      if (this.options.page) params.set("page", this.options.page);
      if (this.options.sortBy) params.set("sort_by", this.options.sortBy);
      if (this.options.sortDesc) params.set("sort_desc", this.options.sortDesc);

      if (this.filterField && (this.filterValue || this.httpMethod)) {
         params.set("filter_field", this.filterField);
         
         params.set("filter_value", 
          this.filterField == 'http_method' ? this.httpMethod : this.filterValue
         );
      }
      
      const request = await fetch(`/api/logs/?${params}`);
      const data = await request.json();
      this.logs = data.results;
      this.totalLogs = data.count;
      this.loading = false;
      this.getStat()
    },
    async getStat(){
      this.loadingStatData = true;
      var params = new URLSearchParams();
      if (this.filterField && (this.filterValue || this.httpMethod)) {
         params.set("filter_field", this.filterField);
         params.set("filter_value", 
          this.filterField == 'http_method' ? this.httpMethod : this.filterValue
         );
      }
      
      const request = await fetch(`/api/stat/?${params}`);
      const data = await request.json();
      this.statData = data.top_ten;
      this.totalLength = data.total_length;
      this.uniqueIP = data.unique_ip;
      this.loadingStatData = false;
    }
  },
  created() {
    this.getData();
  },
  watch: {
    options: function() {
      this.getData();
    }
  }
};
</script>
