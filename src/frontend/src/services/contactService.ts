import { client } from '../api/client';

export interface ContactFormData {
    first_name: string;
    last_name: string;
    email: string;
    phone?: string;
    message: string;
}

export interface ContactResponse {
    success: boolean;
    message: string;
}

export const contactService = {
    /**
     * Send contact form data to the backend.
     * @param data ContactFormData
     * @returns Promise<ContactResponse>
     */
    sendContactForm: async (data: ContactFormData): Promise<ContactResponse> => {
        try {
            console.log('🚀 [ContactService] Sending contact form:', data);

            const response = await client.post<ContactResponse>('/contact/', data);

            console.log('✅ [ContactService] Response received:', response);

            // Client interceptor returns response.data directly, so 'response' here IS the data if successful
            // However, depending on client.ts setup, sometimes it returns the full axios object.
            // Based on previous files, client.ts interceptor returns `response.data`.
            // Let's assume response IS the payload.
            return response as unknown as ContactResponse;

        } catch (error: any) {
            console.error('❌ [ContactService] Error sending contact form:', error);
            if (error.response) {
                console.error('   Running Status:', error.response.status);
                console.error('   Response Data:', error.response.data);
            }
            throw error;
        }
    }
};
