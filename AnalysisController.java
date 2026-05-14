package com.phishing.controller;

import com.phishing.service.PythonIntegrationService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

@RestController
@RequestMapping("/api")
public class AnalysisController {

    private final PythonIntegrationService pythonIntegrationService;

    @Autowired
    public AnalysisController(PythonIntegrationService pythonIntegrationService) {
        this.pythonIntegrationService = pythonIntegrationService;
    }

    @PostMapping("/analyze")
    public ResponseEntity<String> analyzeUrl(@RequestBody Map<String, String> payload) {
        String url = payload.get("url");
        if (url == null || url.trim().isEmpty()) {
            return ResponseEntity.badRequest().body("{\"error\": \"URL is required\"}");
        }

        String result = pythonIntegrationService.analyzeUrl(url);
        return ResponseEntity.ok(result);
    }
}
