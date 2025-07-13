// import { useEffect } from 'react'
// import { useSearchParams, useNavigate } from 'react-router-dom'
// import axios from 'axios'

// const PaymentSuccess = ({ token }) => {
//   const [params] = useSearchParams()
//   const navigate = useNavigate()

//   useEffect(() => {
//     const seatId = params.get('seatId')
//     const busId = params.get('busId')
//     const userId = params.get('userId')

//     const confirmBooking = async () => {
//       try {
//         await axios.post(
//           'http://localhost:8000/api/booking/',
//           { seat: seatId },
//           {
//             headers: {
//               Authorization: `Token ${token}`,
//             },
//           }
//         )
//         alert('Booking confirmed!')
//         navigate('/my-bookings')
//       } catch (error) {
//         alert('Booking failed after payment')
//       }
//     }

//     confirmBooking()
//   }, [])

//   return <div>Processing your booking...</div>
// }

// export default PaymentSuccess




// import { useEffect, useState } from 'react';
// import { useSearchParams, useNavigate } from 'react-router-dom';
// import axios from 'axios';

// const PaymentSuccess = ({ token }) => {
//   const [params] = useSearchParams();
//   const navigate = useNavigate();
//   const [bookingStatus, setBookingStatus] = useState('processing'); // 'processing' | 'success' | 'error'
//   const [bookingDone, setBookingDone] = useState(false);

//   useEffect(() => {
//     const seatId = params.get('seatId');
//     const busId = params.get('busId');
//     const userId = params.get('userId');

//     const confirmBooking = async () => {
//       if (!token || !seatId || bookingDone) return;

//       try {
//         await axios.post(
//           'http://localhost:8000/api/booking/',
//           { seat: seatId },
//           {
//             headers: {
//               Authorization: `Token ${token}`,
//             },
//           }
//         );
//         setBookingStatus('success');
//         setBookingDone(true);
//         // Optional: navigate to bookings after delay
//         setTimeout(() => navigate('/my-bookings'), 1500);
//       } catch (error) {
//         console.error('Booking error:', error);
//         setBookingStatus('error');
//       }
//     };

//     confirmBooking();
//   }, [params, token, bookingDone, navigate]);

//   return (
//     <div className="flex flex-col items-center justify-center min-h-screen p-4">
//       {bookingStatus === 'processing' && (
//         <div className="text-lg font-semibold">⏳ Processing your booking...</div>
//       )}
//       {bookingStatus === 'success' && (
//         <div className="text-green-600 text-xl font-bold">
//           ✅ Booking confirmed!
//         </div>
//       )}
//       {bookingStatus === 'error' && (
//         <div className="text-red-600 text-xl font-bold">
//           ❌ Booking failed after payment. Please contact support.
//         </div>
//       )}
//     </div>
//   );
// };






// // payment-success.jsx (React)
// useEffect(() => {
//   const confirmBooking = async () => {
//     const seatId = new URLSearchParams(window.location.search).get("seatId");
//     const busId = new URLSearchParams(window.location.search).get("busId");
//     const token = localStorage.getItem("token");

//     const response = await fetch("http://localhost:8000/api/confirm-booking/", {
//       method: "POST",
//       headers: {
//         "Content-Type": "application/json",
//         Authorization: `Token ${token}`
//       },
//       body: JSON.stringify({ seatId, busId })
//     });

//     const data = await response.json();
//     console.log("Booking confirmed:", data);
//   };

//   confirmBooking();
// }, []);


// export default PaymentSuccess;






// import { useEffect, useState } from 'react';
// import { useSearchParams, useNavigate } from 'react-router-dom';
// import axios from 'axios';

// const PaymentSuccess = () => {
//   const [params] = useSearchParams();
//   const navigate = useNavigate();
//   const [bookingStatus, setBookingStatus] = useState('processing');

//   useEffect(() => {
//     const seatId = params.get('seatId');
//     const busId = params.get('busId');
//     const token = localStorage.getItem('token');

//     const confirmBooking = async () => {
//       if (!token || !seatId || !busId) {
//         setBookingStatus('error');
//         return;
//       }

//       try {
//         await axios.post(
//           'http://localhost:8000/api/confirm-booking/',
//           { seatId, busId },
//           {
//             headers: {
//               'Content-Type': 'application/json',
//               Authorization: `Token ${token}`,
//             },
//           }
//         );
//         setBookingStatus('success');
//         setTimeout(() => navigate('/my-bookings'), 1500);
//       } catch (error) {
//         console.error('Booking confirmation failed:', error);
//         setBookingStatus('error');
//       }
//     };

//     confirmBooking();
//   }, [params, navigate]);

//   return (
//     <div className="flex flex-col items-center justify-center min-h-screen p-4">
//       {bookingStatus === 'processing' && (
//         <div className="text-lg font-semibold">⏳ Processing your booking...</div>
//       )}
//       {bookingStatus === 'success' && (
//         <div className="text-green-600 text-xl font-bold">
//           ✅ Booking confirmed!
//         </div>
//       )}
//       {bookingStatus === 'error' && (
//         <div className="text-red-600 text-xl font-bold">
//           ❌ Booking failed after payment. Please contact support.
//         </div>
//       )}
//     </div>
//   );
// };

// export default PaymentSuccess;









import { useEffect, useRef, useState } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import axios from 'axios';

const PaymentSuccess = ({ token }) => {
  const [params] = useSearchParams();
  const navigate = useNavigate();
  const [bookingStatus, setBookingStatus] = useState('processing');
  const alreadyBooked = useRef(false); // ✅ prevents duplicate requests

  useEffect(() => {
    const seatId = params.get('seatId');
    const busId = params.get('busId');

    const confirmBooking = async () => {
      if (!token || alreadyBooked.current) return;
      alreadyBooked.current = true;

      try {
        const response = await axios.post(
          'http://localhost:8000/api/confirm-booking/',
          { seatId, busId },
          {
            headers: {
              Authorization: `Token ${token}`,
            },
          }
        );
        console.log("Booking success:", response.data);
        setBookingStatus('success');
        setTimeout(() => navigate('/my-bookings'), 1500);
      } catch (error) {
        console.error("Booking failed:", error.response?.data || error.message);
        setBookingStatus('error');
      }
    };

    confirmBooking();
  }, [params, token, navigate]);

  return (
    <div className="flex flex-col items-center justify-center min-h-screen p-4">
      {bookingStatus === 'processing' && (
        <div className="text-lg font-semibold">⏳ Processing your booking...</div>
      )}
      {bookingStatus === 'success' && (
        <div className="text-green-600 text-xl font-bold">
          ✅ Booking confirmed!
        </div>
      )}
      {bookingStatus === 'error' && (
        <div className="text-red-600 text-xl font-bold">
          ❌ Booking failed after payment. Please contact support.
        </div>
      )}
    </div>
  );
};

export default PaymentSuccess;
