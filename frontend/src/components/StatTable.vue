<template>
  <v-simple-table>
    <template v-slot:default>
      <thead>
        <tr>
          <th class="text-left">IP Address</th>
          <th class="text-left">Count</th>
          <th class="text-left">GET</th>
          <th class="text-left">POST</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in data" :key="item.ip_address">
          <td>{{ item.ip_address }}</td>
          <td>{{ item.count }}</td>
          <td>{{ item.GET }}</td>
          <td>{{ item.POST }}</td>
        </tr>
      </tbody>
    </template>
  </v-simple-table>
</template>

<script>
export default {
  props: ['data'],
  name: "StatTable"
}
</script>