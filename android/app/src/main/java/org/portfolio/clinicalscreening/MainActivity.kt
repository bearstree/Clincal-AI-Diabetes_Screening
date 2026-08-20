package org.portfolio.clinicalscreening

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.unit.dp
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext

class MainActivity : ComponentActivity() {
    override fun onCreate(state: Bundle?) {
        super.onCreate(state)
        setContent { MaterialTheme { ScreeningApp() } }
    }
}

@Composable
fun ScreeningApp() {
    var age by remember { mutableStateOf("") }; var waist by remember { mutableStateOf("") }
    var diastolic by remember { mutableStateOf("") }; var active by remember { mutableStateOf<Boolean?>(null) }
    var result by remember { mutableStateOf<Prediction?>(null) }; var message by remember { mutableStateOf("") }
    var loading by remember { mutableStateOf(false) }; val scope = rememberCoroutineScope()
    val valid = age.toIntOrNull() in 20..80 && waist.toDoubleOrNull()?.let { it in 40.0..200.0 } == true &&
        diastolic.toDoubleOrNull()?.let { it in 20.0..160.0 } == true && active != null

    Scaffold { padding ->
        Column(Modifier.padding(padding).verticalScroll(rememberScrollState()).padding(24.dp), verticalArrangement = Arrangement.spacedBy(16.dp)) {
            Text("Diabetes screening research tool", style = MaterialTheme.typography.headlineLarge)
            Text("Educational research only—not a diagnosis or medical advice.", color = MaterialTheme.colorScheme.error)
            NumberField("Age (20–80 years)", age) { age = it }
            NumberField("Waist circumference (40–200 cm)", waist) { waist = it }
            NumberField("Diastolic blood pressure (20–160 mmHg)", diastolic) { diastolic = it }
            Text("Physically active")
            Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                FilterChip(active == true, { active = true }, { Text("Yes") })
                FilterChip(active == false, { active = false }, { Text("No") })
            }
            Button(enabled = valid && !loading, onClick = {
                loading = true; message = "Estimating…"; result = null
                scope.launch {
                    runCatching { withContext(Dispatchers.IO) { ApiClient.predict(age.toInt(), waist.toDouble(), active!!, diastolic.toDouble()) } }
                        .onSuccess { result = it; message = "" }.onFailure { message = "Service unavailable. Try again later." }
                    loading = false
                }
            }) { Text("Estimate research probability") }
            if (message.isNotEmpty()) Text(message)
            result?.let {
                HorizontalDivider(); Text("${(it.probability * 100).format1()}%", style = MaterialTheme.typography.displayMedium)
                Text(if (it.aboveThreshold) "Above the model's validation threshold." else "Below the model's validation threshold.")
                Text("Model ${it.version} · threshold ${(it.threshold * 100).format1()}%")
                Text("The threshold is not a clinical diagnosis or treatment boundary.", style = MaterialTheme.typography.bodySmall)
            }
        }
    }
}

@Composable private fun NumberField(label: String, value: String, change: (String) -> Unit) =
    OutlinedTextField(value, change, Modifier.fillMaxWidth(), label = { Text(label) }, singleLine = true, keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Decimal))

private fun Double.format1() = String.format("%.1f", this)
