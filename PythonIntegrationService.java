package com.phishing.service;

import org.springframework.stereotype.Service;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.nio.file.Paths;

@Service
public class PythonIntegrationService {

    public String analyzeUrl(String url) {
        StringBuilder output = new StringBuilder();
        try {
            // Path to the python script
            String scriptPath = Paths.get("python_engine", "detector.py").toAbsolutePath().toString();
            
            // Execute python script. We assume 'python' is in the system PATH.
            ProcessBuilder pb = new ProcessBuilder("python", scriptPath, url);
            pb.redirectErrorStream(true);
            Process process = pb.start();

            BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
            String line;
            while ((line = reader.readLine()) != null) {
                output.append(line);
            }
            
            int exitCode = process.waitFor();
            if (exitCode != 0) {
                return "{\"error\": \"Python script exited with code " + exitCode + "\"}";
            }
            
            return output.toString();
        } catch (Exception e) {
            e.printStackTrace();
            return "{\"error\": \"Exception occurred while calling Python script: " + e.getMessage() + "\"}";
        }
    }
}
