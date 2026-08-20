package org.portfolio.clinicalscreening

import java.net.HttpURLConnection
import java.net.URL
import org.json.JSONObject

data class Prediction(val probability: Double, val threshold: Double, val aboveThreshold: Boolean, val version: String)

object ApiClient {
    fun predict(age: Int, waist: Double, active: Boolean, diastolic: Double): Prediction {
        val connection = URL("${BuildConfig.API_BASE_URL.trimEnd('/')}/v1/predict").openConnection() as HttpURLConnection
        connection.requestMethod = "POST"
        connection.connectTimeout = 10_000
        connection.readTimeout = 10_000
        connection.setRequestProperty("Content-Type", "application/json")
        connection.doOutput = true
        val body = JSONObject().put("age_years", age).put("waist_cm", waist)
            .put("physically_active", active).put("diastolic_bp", diastolic)
        connection.outputStream.use { it.write(body.toString().toByteArray()) }
        val stream = if (connection.responseCode in 200..299) connection.inputStream else connection.errorStream
        val response = stream.bufferedReader().use { it.readText() }
        if (connection.responseCode !in 200..299) error("API returned ${connection.responseCode}")
        val json = JSONObject(response)
        return Prediction(json.getDouble("probability"), json.getDouble("threshold"), json.getBoolean("above_validation_threshold"), json.getString("model_version"))
    }
}
