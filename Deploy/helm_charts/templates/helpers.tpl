{{- define "helpers.list-env-variables"}}
{{- range $key, $val := .Values.image.env }}
- name: {{ $key }}
  value: {{ $val | quote }}
{{- end}}
{{- end }}
