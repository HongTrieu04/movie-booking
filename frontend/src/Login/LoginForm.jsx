import { useState, useEffect } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { Button, Checkbox, Form, Input, Divider, message } from "antd";

function LoginForm() {
  const navigate = useNavigate();
  const location = useLocation();
  const [loading, setLoading] = useState(false);

  // --- Login bằng DB ---
  const handleLogin = async (values) => {
    setLoading(true);
    try {
      const res = await fetch("/api/auth/login-db", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(values),
      });
      if (!res.ok) throw new Error("Sai email hoặc mật khẩu");

      const data = await res.json();
      localStorage.setItem("access_token", data.access_token);

      const meRes = await fetch("/api/auth/me", {
        headers: { Authorization: `Bearer ${data.access_token}` },
      });
      const meData = await meRes.json();
      console.log("User info:", meData);

      message.success("Đăng nhập thành công!");
      navigate("/");
    } catch (err) {
      message.error(err.message);
    } finally {
      setLoading(false);
    }
  };

  // --- Redirect tới Google ---
  const handleGoogleLogin = () => {
    const googleClientId = process.env.REACT_APP_GOOGLE_CLIENT_ID;
    const redirectUri = process.env.REACT_APP_GOOGLE_REDIRECT_URI;
    const scope = "openid email profile";

    const authUrl = `https://accounts.google.com/o/oauth2/v2/auth?client_id=${googleClientId}&redirect_uri=${encodeURIComponent(
      redirectUri
    )}&response_type=code&scope=${encodeURIComponent(scope)}`;

    window.location.href = authUrl;
  };

  // --- Xử lý Google callback ---
  useEffect(() => {
    const params = new URLSearchParams(location.search);
    const code = params.get("code");
    if (code) {
      (async () => {
        try {
          setLoading(true);
          const res = await fetch(`/api/auth/login-google?code=${code}`);
          if (!res.ok) throw new Error("Google login thất bại");

          const data = await res.json();
          localStorage.setItem("access_token", data.access_token);

          const meRes = await fetch("/api/auth/me", {
            headers: { Authorization: `Bearer ${data.access_token}` },
          });
          const meData = await meRes.json();
          console.log("User info:", meData);

          message.success("Đăng nhập Google thành công!");
          navigate("/");
        } catch (err) {
          message.error(err.message);
        } finally {
          setLoading(false);
        }
      })();
    }
  }, [location]);

  return (
    <div
      style={{
        maxWidth: 400,
        margin: "50px auto",
        padding: 24,
        border: "1px solid #f0f0f0",
        borderRadius: 8,
        boxShadow: "0 2px 8px rgba(0,0,0,0.1)",
      }}
    >
      <h2 style={{ textAlign: "center", marginBottom: 24 }}>Đăng nhập</h2>

      <Form layout="vertical" onFinish={handleLogin}>
        <Form.Item
          label="Email"
          name="email"
          rules={[{ required: true, message: "Vui lòng nhập email!" }]}
        >
          <Input />
        </Form.Item>

        <Form.Item
          label="Mật khẩu"
          name="password"
          rules={[{ required: true, message: "Vui lòng nhập mật khẩu!" }]}
        >
          <Input.Password />
        </Form.Item>

        <Form.Item name="remember" valuePropName="checked">
          <Checkbox>Ghi nhớ đăng nhập</Checkbox>
        </Form.Item>

        <Button
          type="primary"
          htmlType="submit"
          block
          loading={loading}
        >
          Đăng nhập bằng Email
        </Button>
      </Form>

      <Divider>Hoặc</Divider>

      <Button
        type="primary"
        block
        style={{
          background: "#db4437",
          borderColor: "#db4437",
          marginBottom: 8,
        }}
        onClick={handleGoogleLogin}
      >
        Đăng nhập với Google
      </Button>

      <Button
        type="default"
        block
        style={{ background: "green", color: "white" }}
        onClick={() => navigate("/register")}
      >
        Đăng ký tài khoản
      </Button>
    </div>
  );
}

export default LoginForm;
