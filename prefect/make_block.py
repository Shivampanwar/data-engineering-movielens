from prefect_gcp import GcpCredentials
from prefect_gcp.cloud_storage import  GcsBucket

# replace this PLACEHOLDER dict with your own service account info
# service_account_info = {
#   "type": "service_account",
#   "project_id": "PROJECT_ID",
#   "private_key_id": "KEY_ID",
#   "private_key": "-----BEGIN PRIVATE KEY-----\nPRIVATE_KEY\n-----END PRIVATE KEY-----\n",
#   "client_email": "SERVICE_ACCOUNT_EMAIL",
#   "client_id": "CLIENT_ID",
#   "auth_uri": "https://accounts.google.com/o/oauth2/auth",
#   "token_uri": "https://accounts.google.com/o/oauth2/token",
#   "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
#   "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/SERVICE_ACCOUNT_EMAIL"
# }

def create_gcp_block():

  service_account_info = {
    "type": "service_account",
    "project_id": "projectmovies-381510",
    "private_key_id": "6f20bdffa6e27076b77bb45108ffa14a9e1cf491",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCRrnXdO6p3t1Vn\nrxh8Egxeld/HSOJ/DFK37aWjlZFJaAG2W2MhwSsKHTZlXWnIkEulE3ZusViOPjO0\n+Asu/O/V7detoMOuaKpuHSUCKmwRabgDHyN86O+Jpser+2gcXA39uReVOpV3Bnuv\nXfJjBSArDmLSV7EtKus6dyXD6RbTbUwfhUM78n2/X9fzKanaCLky6pacBmEcQCM1\nTjOO8rQhkjaZSzVtgTJFTOuWS7fO6OqIGKfUMYiHNJcrMF1Mf877aiK8McbxN3rG\n+Nc4WWDelBUYMqXgfrom5Rlnc40aNmm6MQ0qnVhoV+wNCBMUDpt2ESSM47eIuHUn\niN/h4X+xAgMBAAECggEAFwx7/7t+birL8OJuOccIkk3HwM8Xwr5vjJklYUXQiEV+\ngTG2np23fQX/2AwY/fn9IIon7T3S2HfKlNcVEeND4Nwcs7mhQW60NEVugwgKNBEU\nDi5hiNQ5KIACIa7eRcpiDk1isqIOXsK1qUUbDIPq7H+orps1iti6Vx7dverFc+rJ\noJMiyrl2m70QBJQwS3S/nGeuRLubTxBCWgZfJoE0cD2SaI3kxVgnFacTGyT1Wour\n2LX0iaB4TN0WBaqw8lr/tPkAzpxopWgJBVeARNBNAugkf4EBjmDGGRP11rIjF+5w\n/CB1fwpH4keacLYvdvhaz17Wd6wAxvJtp9lIMABgHwKBgQDLMhMc4HE78T0MkyLk\nyoUp9MB9a9KtxyNKdmyR1nSFiGeaJSW5xHyRJ7Yx+Z2e5whZhCyOEcYmHT6OFTJW\nkOkSly0Cbm7yDOWzGi5Q7cemZpq+tIvBNX9BpyI82Lv1TBCb0yF2L08xRme0FeUp\nEb6AObZILUwJAmPmetvjl+irVwKBgQC3iinWg/TNpzeVtIRApNBHtbYfvtXmg3HZ\no8iMDw2lKHSAtTySafFXKdKR34mMgFZsgbtbkBX8Ve/KugXx1g+wBulwUsSGU51b\nH3kDlQOkKSlkwDEUA0AL3Yi6djOCkhotfF398MOp73UGirSuDzSJs+r0xTgECq5L\n6nRF6wLQNwKBgEGkp7AIggxPXt2VGwy2sFZhj131W1ZwouIHaAOlOHd7HZ0aqxlc\ndLGgFqgGb/lJwdTJcmtjKpRdljvodR6qKeGrnQrQCl9/8yTtLFFQv9LuCsfZI90D\nH11iVRk7G12feS4eAw1fM0JD8HSpLiMabGSYQF8I4yt17jgjMK5SAQR5AoGAYVpN\nutUfYn4Rw7yOceN5/q9pvQjyWGTcXL69P100tafxs9tuF5NOSheK84kIYpgoP0HI\n6VZR8xh6KqPlR1Nt2savx75/M2jijFTzUW0XE1op9KDk52KZ9DE7tvu/csCgVgQj\nrvCoOFklT6T/FVxHV8sxE0gQ4EPyE552sidnxJ0CgYEAu2FmgELrzUOadxpY2Al6\ny6OjTnjBfE1V2queumB0srceAoOZ/bLOLaxEDiysQ6mJOyx/1tK1rqEnu89j1j9e\nx+iV1C8ks1puY2f90EIQSYHdjTtstcEzjdso5I19ZUaKskKm7bX+5V8yohrzM3Lk\nlCKmLi6pzbFx/d8cFYNCWNg=\n-----END PRIVATE KEY-----\n",
    "client_email": "movie-project-user@projectmovies-381510.iam.gserviceaccount.com",
    "client_id": "107696121996799995644",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/movie-project-user%40projectmovies-381510.iam.gserviceaccount.com"
  }

  GcpCredentials(
      service_account_info=service_account_info
  ,).save("gcp-block",overwrite=True)
  return True