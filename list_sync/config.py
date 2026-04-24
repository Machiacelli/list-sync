def test_overseerr_api(overseerr_url, api_key=None):
    """Test Seer connection using session login instead of API key."""
    spinner = Halo(text=color_gradient("🔍  Testing API connection...", "#ffaa00", "#ff5500"), spinner="dots")
    spinner.start()

    try:
        session = requests.Session()

        # 🔥 LOGIN istället för API key
        email = os.getenv("SEER_EMAIL")
        password = os.getenv("SEER_PASSWORD")

        if not email or not password:
            raise Exception("Missing SEER_EMAIL or SEER_PASSWORD")

        login = session.post(
            f"{overseerr_url}/api/v1/auth/login",
            json={"email": email, "password": password}
        )

        if login.status_code != 200:
            raise Exception(f"Login failed: {login.text}")

        response = session.get(f"{overseerr_url}/api/v1/status")
        response.raise_for_status()

        spinner.succeed(color_gradient("🎉  Seer connection successful!", "#00ff00", "#00aa00"))

    except Exception as e:
        spinner.fail(color_gradient(f"❌  Seer connection failed: {str(e)}", "#ff0000", "#aa0000"))
        raise
