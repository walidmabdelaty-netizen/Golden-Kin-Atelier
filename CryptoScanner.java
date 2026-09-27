import java.security.Provider;
import java.security.Security;
import java.util.Set;
import java.util.TreeSet;

public class CryptoScanner {
    public static void main(String[] args) {
        System.out.println("[*] SCANNING JAVA SECURITY PROVIDERS...\n");
        
        Set<String> ciphers = new TreeSet<>();
        Set<String> hashes = new TreeSet<>();
        Set<String> keyAgreements = new TreeSet<>();
        
        // المرور على جميع مزودي الأمان في بيئة جافا الحالية
        for (Provider provider : Security.getProviders()) {
            for (Provider.Service service : provider.getServices()) {
                String type = service.getType();
                String algo = service.getAlgorithm();
                
                if (type.equals("Cipher")) {
                    ciphers.add(algo);
                } else if (type.equals("MessageDigest")) {
                    hashes.add(algo);
                } else if (type.equals("KeyAgreement")) {
                    keyAgreements.add(algo);
                }
            }
        }
        
        System.out.println("--- MILITARY-GRADE CIPHERS (Encryption) ---");
        // فلترة وعرض خوارزميات التشفير القوية فقط
        ciphers.stream()
               .filter(c -> c.contains("AES") || c.contains("ChaCha") || c.contains("RSA"))
               .forEach(c -> System.out.println(" ✔ " + c));
               
        System.out.println("\n--- SECURE HASHES (NIST Approved) ---");
        // فلترة وعرض خوارزميات التجزئة المعتمدة
        hashes.stream()
              .filter(h -> h.contains("SHA-256") || h.contains("SHA-3") || h.contains("SHA-512"))
              .forEach(h -> System.out.println(" ✔ " + h));
              
        System.out.println("\n--- KEY EXCHANGE ALGORITHMS ---");
        keyAgreements.stream()
                     .forEach(k -> System.out.println(" ✔ " + k));

        System.out.println("\n[i] Post-Quantum Note: If algorithms like 'Kyber' or 'Dilithium' are not listed above,");
        System.out.println("    we will need to integrate the 'BouncyCastle PQC' provider in the next architectural step.");
    }
}
